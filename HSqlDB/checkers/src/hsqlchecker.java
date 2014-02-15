import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class hsqlchecker {
	
	public static boolean isNull(String str) {
        return str == null ? true : false;
    }

    public static boolean isNullOrBlank(String param) {
        if (isNull(param) || param.trim().length() == 0) {
            return true;
        }
        return false;
    }
	
	public static void main(String[] args) throws SQLException, FileNotFoundException, UnsupportedEncodingException
	{
		try 
		{
			Class.forName("org.hsqldb.jdbc.JDBCDriver");
		} 
		catch (ClassNotFoundException e)
		{
			System.out.println(e.getMessage());
		}
		
		Connection con = null;
		int expectedCount = 100;
        try
        {
        	//String str = "jdbc:hsqldb:file:/home/ramnatthan/workspace/HSqlApp/databases/mydatabase";
        	String str = "jdbc:hsqldb:file:/home/ramnatthan/workload_snapshots/hsqldb/replayedsnapshot/mydatabase";
        	con = DriverManager.getConnection(str);        	
            PreparedStatement pst=con.prepareStatement("select * from contacts");
            pst.clearParameters();
            ResultSet rs=pst.executeQuery();
            boolean notProper = false;
       
            int c = 0;
            while(rs.next()){
            	c++;
            	
            	String one = rs.getString(1);
            	String two = rs.getString(2);
            	String three = rs.getString(3);
            	
            	if(isNullOrBlank(one) || isNullOrBlank(two) || isNullOrBlank(three))
            	{
            		notProper = true;
            	}
            	if(!one.startsWith("name") || !two.startsWith("email"))
            	{
            		notProper = true;
            	}
            	
                System.out.print(one + "-");
                System.out.print(two + "-");
                System.out.print(three);
                
                System.out.println();
            }
            
            if(c!=0 && c != expectedCount+1 ) notProper = true;
            
            PrintWriter writer = new PrintWriter("/tmp/short_output", "UTF-8");
            String op = notProper ? "Improper Data - Problematic!":"No problem!";
            writer.println(op);
            writer.close();
            
        	con.close();
        } 
        catch(Exception e)
        {
        	PrintWriter writer = new PrintWriter("/tmp/short_output", "UTF-8");
        	if(e != null && e.getMessage() != null)
        	{
        		writer.write(e.getMessage());
        	}
        	
            e.printStackTrace();
            writer.close();
            //System.out.println(e.getMessage());
        }
 		
		System.out.println("Done");
	}
}
