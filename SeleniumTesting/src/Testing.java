/*
 * @Author: A. Danielle Talley
 * @Last Modification: 24th April 2016
 * 
 * This Java project will automatically sign in a user to Google Calendar and 
 * enter in calendar events. 
 * This has only been tested with Chrome.
 */
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Testing {
	//Constant Variables
	public static final String DELIMITER ="\t";
	public static final String FILENAME = "src\\testInputs.txt";
	//Mallable Variables
	public static ArrayList<Event> events;
	
	//read the input file and populate the "events" array
	public static void readEventList(){
		System.out.println("Clearing /'Events/'");
		events.clear();
		System.out.println("Reading Input File");
		int numOfEvents = 0;
		try{
			
			BufferedReader inputFile = new BufferedReader(new FileReader(FILENAME));
			String line;
			while((line = inputFile.readLine()) != null){
				String[] information = line.split(DELIMITER);
				if(information.length == 6){
					//String aName, String aDate, String aLocation, boolean isAllDay, String aStartTime, String aEndTime){
					Event e = new Event(information[0], information[1], information[2], information[3], information[4], information[5]);
					events.add(e);
					numOfEvents++;
				}
			}
			inputFile.close();
		} catch(IOException e){
			System.out.println(e.getMessage());
			return;
		}
		System.out.println("Successfully added "+numOfEvents+" events");
		
	}
	
	

	public static void main(String[] args) {
		events = new ArrayList<Event>();
		//populate the events list
		readEventList(); 
		
		//open a browser to google calendars
		GoogleCalendar calendar = new GoogleCalendar(true); 
		//Auto login the user
		calendar.LogIn("immaCalendarBot", "yeahRobot111"); 
		//add all the events
		for(Event e : events){
			calendar.createEvent(e);
		}
		//Add an event using the Quick Event feature on the main menu
		calendar.createQuickEvent(new Event("Bar Hopping", "04/30/2016", "The Vista", true, "9:00pm", "11:59pm"));		
		//End the current session. If you want it to close the browser, change it to "true"
		calendar.endSession(false);
		System.out.println("Ending Testing");
	}//end Main

}//end Testing



/*
 * Other Things I Tried
 * 
*/
