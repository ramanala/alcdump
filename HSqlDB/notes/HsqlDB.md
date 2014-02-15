Write protocol
--------------

Protocol to ensure consistency : HSqlDB uses a slight variation of the write ahead logging protocol. It logs the exact sql operations to the log file when a transaction is committed. The amount of data going to the log file is proportional to the data being written as part of the transaction. So this write can span many pages. 

HSqlDb calls the actual database file as script file. For the sake of consistency, we will also use the same name through out this notes. After writing to the log and syncing it, a new file called script.new is created and all data is written again to it and then synced. HSqlDB uses a file called the properties file which essentially contains information about the current state of the database. After writing to the script.new file, a new properties file called properties.new is created and a piece of information to denote about the presence of a new script.new file is written to the properties.new file. The properties.new file is synced. After this, the old properties file is unlinked and the properties.new file is renamed to properties. After this, the log file and old script file are unlinked. After this step, the script.new file is renamed to script. To indicate the change, a piece of information is written to properties.new file. Finally the properties.new file is renamed to properties.

To reiterate, these are the following steps when a transaction is committed to the database:

Note that there is a old properties file for the database and there is a old script file as well. 

1. Write to database.log file. Fsync it.
2. Copy data from database.log to script.new (It is kind of checkpoint-ing the transaction). Fsync the script.new file.
3. Create and write to properties.new about the changes. 
4. Unlink old properties file.
5. rename properties.new to properties.
6. unlink script(old) and log file.
7. rename script.new to script.
8. create properties.new for saying that we don't have any new files.
9. unlink properties and rename properties.new to properties.

Assumptions and Vulnerabilities
-------------------------------

1. Atomicity of log writes - As mentioned earlier, HSqlDB uses write ahead logging to ensure consistency. The write to the log can span many pages and hence can be split. In our simple workload, the log write of ~6KB was found in the traces. HSqlDB assumes this write to be atomic and also be ordered even if it split into many writes. If the atomiticity is broken and the broken operations are reordered, the database will get into a corrupted state. This bug is straight forward to reproduce. The effect is worse as the user of the database will see corrupted values when retrieving data from the database.

2. Reordering renames and unlinks - HSqlDB uses the steps mentioned in section 1 to transition from one consistent state to the next consistent state. There is a sequence of operation like the below in the flow:

a. unlink(properties)
b. rename(properties.new to properties)
c. unlink(old script)
d. unlink(log)

In the above sequence, if operations c and d happen before operation b, the database gets into a bad state. The effect is worse as subsequent opens of the database will fail with and error something like this: "java.sql.SQLException: java.io.FileNotFoundException: /home/ramnatthan/workload_snapshots/hsqldb/replayedsnapshot/mydatabase.script (No such file or directory)"

3. This vulnerability is similar to the first one. HSqlDB(JDBC to be precise) offers a feature called 'savepoints'. When running a big transaction, the program can set savepoints on the state of the database. If the application decides to rollback the transaction for some reason, it has now options to rollback upto a specific savepoint. We tested this scenario and observed that database can get to a corrupted state very similar to the first vulnerability. 

4. This vulnerability is regarding the lock file created by the database. When a database is opened, HSqlDB creates a lock file to gaurantee some sort of isolation (I am not sure exactly why this is done). The lock file is created and 15 bytes are written to it one byte at a time (so 15 write calls). If an application crash happens in between these writes, the database will be left in a bad state. Subsequent opens of the database will throw errors something like this: "java.sql.SQLException: Database lock acquisition failure: lockFile: org.hsqldb.persist.LockFile@de7c9b34[file =/home/ramnatthan/workload_snapshots/hsqldb/replayedsnapshot/mydatabase.lck, exists=true, locked=false, valid=false, ] method: checkHeartbeat length: 9

Workloads and checkers
----------------------

HSqlDB is accessed through JDBC API. It supports transactional and non-transaction interaction. Since the non-transactional API does not give any guarantee about consistency, our workloads were transactional. 

HSqlDB supports two main types of tables: 1. Cached tables and 2. Memory tables. In memory tables, the entire database is deserialized into memory on open of the database from the disk. In cached tables, only the indexed columns are loaded into memory.

The workload is very simple. It starts a transaction, creates a table and inserts 100 rows into the database as part of a transactions and then commits the transaction. Few variations like rollback and savepoints were also done. The workloads were run for both types of tables. 

The checker is also very simple. It opens the database and retrieves data from the database. It checks if the rows retrieved are complete and correct. For example the checker will assert if the number of rows is not as expected or if it was able to retrieve some garbage data from the database. 

Other bugs and issues 
---------------------

The below bugs show that HSqlDB can actually get to a corrupt state like we have seen in our testing:

http://hsqldb.10974.n7.nabble.com/Recovering-corrupted-database-td1035.html
http://sourceforge.net/p/hsqldb/discussion/73674/thread/002a56d2