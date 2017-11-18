/*
 * Sprout: R&B Tree Creator
 * Created by Audrey "Danielle" Talley
 * 18 March 2015
 *  
 * This is the main driver for the red and black tree creator.
 * Running it is pretty straight forward.
 */

import java.util.Scanner;
public class frontEnd {

	private static String DELIMETER = " ";
	public static char dataType;
	private static char INTEGER = 'i';
	private static char DOUBLE = 'd';
	private static char STRING = 's';
	private static char CHARACTER = 'c';
	public static binaryTree TREE = new binaryTree();
	
	private static boolean checkDataType(String data, char dataType)
	{
		if(dataType == INTEGER)
		{
			try
			{
				Integer.parseInt(data);
				return true;
			}
			catch(Exception e)
			{
				System.out.println("You can only enter integers");
				return false;
			}
		}
		else if(dataType == DOUBLE)
		{
			try
			{
				Double.parseDouble(data);
				return true;
			}
			catch(Exception e)
			{
				System.out.println("You can only enter doubles");
				return false;
			}
		}
		else if(dataType == CHARACTER)
		{
			if(data.length() != 1)
			{
				System.out.println("You can only enter characters");
				return false;
			}
			else
			{
				return true;
			}
		}
		else if(dataType == STRING)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	
	private static char setDataType(char dataType)
	{
		Scanner keyboard = new Scanner(System.in);
		dataType = 'a';
		System.out.println("What kind of data do you want to sort?");
		while(dataType == 'a')
		{
			System.out.println("Please enter \"i\" for Integer, \"d\" for Double, \"c\" for Character, and \"s\" for String.");
			String input = keyboard.nextLine();
			if(input.toLowerCase().charAt(0) == 'c')
			{
				dataType = CHARACTER;
			}
			else if(input.toLowerCase().charAt(0) == 'i')
			{
				dataType = INTEGER;
			}
			else if(input.toLowerCase().charAt(0) == 'd')
			{
			dataType = DOUBLE;
			}
			else if(input.toLowerCase().charAt(0) == 's')
			{
				dataType = STRING;
			}
			else
			{
				System.out.println("Data type not recognized");
			}
		}
		System.out.println("\n<Planting Tree>\n");
		return dataType;
	}
	
	
	private static void dataEntry(char dataType)
	{
		
		Scanner keyboard = new Scanner(System.in);
		System.out.println("Please enter data separated by spaces!");
		String input = keyboard.nextLine();
		String [] inputArray = input.split(DELIMETER);
		System.out.println("\n<Growing Tree>\n");
		for(String data: inputArray)
		{
			if(checkDataType(data, dataType))
			{
				TREE.insert(data);
			}
			else
			{
				System.out.println("This data ("+data+") was not inserted because it did not have the correct data type");
			}
		}
	}
	
	
	private static void deleteData(char dataType)
	{
		
		Scanner keyboard = new Scanner(System.in);
		System.out.println("Please enter the data you want to delete");
		String input = keyboard.nextLine();
		if(checkDataType(input, dataType))
		{
			System.out.println("\n<Pruning Tree>\n");
			TREE.delete(input);
		}
		else
		{
			System.out.println("This data ("+input+") was not deleted because it did not have the correct data type");
		}
	}
	
	private static void start(boolean init)
	{
		if(!init)
		{
			System.out.println("\n<Chopping Tree>");
		}
		TREE.clearAll();
		dataType = setDataType(dataType);
		dataEntry(dataType);
	}
	
	
	
	public static void main(String[] args) {
		System.out.println("Welcome to Sprout: R&B Tree Creator!!");
		System.out.println("Please keep fingers crossed at all times");
		System.out.println();
		start(true);
		System.out.println();
		boolean toContinue = true;
		
		while(toContinue)
		{
			System.out.println("Now what would you like to do?");
			System.out.println("Type \"i\" to insert data");
			System.out.println("Type \"d\" to delete data");
			System.out.println("Type \"c\" to clear the current tree and start a new one");
			System.out.println("Type \"p\" to print the tree");
			System.out.println("Or type \"q\" to quit");
			
			
			Scanner keyboard = new Scanner(System.in);
			String input = keyboard.nextLine();
			if(input.equalsIgnoreCase("i"))
			{
				dataEntry(dataType);
			}
			else if(input.equalsIgnoreCase("d"))
			{
				deleteData(dataType);
			}
			else if(input.equalsIgnoreCase("c"))
			{
				System.out.println("Are you sure you want to clear the tree? (type \"y\" for yes or \"n\" for no)");
				input = keyboard.nextLine();
				if(input.equalsIgnoreCase("y"))
				{
					start(false);
				}
			}
			else if(input.equalsIgnoreCase("p"))
			{
				System.out.println("\n<Admiring Tree>\n");
				TREE.writeOutput();
			}
			else if(input.equalsIgnoreCase("q"))
			{
				toContinue = false;
			}

			else
			{
				System.out.println("Input not recognized");
			}
			System.out.println();
		}

		System.out.println("Thanks for growing!");

		
		
		
		
		
		

	}

}
