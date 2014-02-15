import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;


public class HSqlApp
{

	public static void main(String[] args) throws SQLException
	{
		if (args.length == 0)
		{
			createinsert.createAndInsert(true, false, false, false);
			//display.dosomething(true);
		}
		else
		{
			
		}
		
		System.out.println("Done");
	}
}

