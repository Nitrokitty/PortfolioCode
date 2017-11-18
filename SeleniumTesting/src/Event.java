/*
 * @Author: A. Danielle Talley
 * @Last Modification: 24th April 2016
 * 
 * This class will save all the information
 * about an event for later use.
 */
public class Event {
	//Variables
	private String name;
	private boolean isAllDay;
	private boolean startBeforeNoon;
	private boolean endsBeforeNoon;
	private String location;
	private String description;
	private int startHour;
	private int startMinutes;
	private int endHour;
	private int endMinutes;
	private int month;
	private int day;
	private int year;
	//Constructors
	public Event(String aName, String aDate, String aLocation, boolean isAllDay, String aStartTime, String aEndTime){
		setName(aName);
		setDate(aDate);
		setLocation(aLocation);
		this.isAllDay = isAllDay;
		if(!isAllDay){
			setStartTime(aStartTime);
			setEndTime(aEndTime);
		}
		else{
			setStartTime("12:00am");
			setEndTime("11:59pm");
		}
		System.out.println("The following event was created successfully: \'" + this.toString() + "\'");
	}
	public Event(String aName, String aDate, String aLocation, String allDay, String aStartTime, String aEndTime){
		setName(aName);
		setDate(aDate);
		setLocation(aLocation);
		if(allDay.equalsIgnoreCase("true")){
			isAllDay = true;
		}
		else
			isAllDay = false;
		if(!isAllDay){
			setStartTime(aStartTime);
			setEndTime(aEndTime);
		}
		else{
			setStartTime("12:00am");
			setEndTime("11:59pm");
		}
		System.out.println("The following event was created successfully: \'" + this.toString() + "\'");
	}
	
	//Getters
	public String getName() {
		return name;
	}
	public boolean isAllDay() {
		return isAllDay;
	}
	public String getLocation() {
		return location;
	}
	public String getDescription() {
		return description;
	}

	//Setters
	public void setName(String name) {
		this.name = name;
	}
	public void setStartTime(String startTime) { //Format: hh:mmxm
		String[] time = startTime.split(":");
		if(time.length != 2 
				|| (time[0].length() != 2 && time[0].length() != 1) 
				|| time[1].length() != 4){
			System.out.println("Start Time Not Set: Invalid number of digits in "+startTime);
			return;
		}
		try{
			startHour = Integer.parseInt(time[0]);
			startMinutes = Integer.parseInt(time[1].substring(0, 2));
			String suffix = time[1].substring(2,4);
			if( suffix.equalsIgnoreCase("am"))
				startBeforeNoon = true;
			else if( suffix.equalsIgnoreCase("pm"))
				startBeforeNoon = false;
			else{
				System.out.println("Invalid suffix \'" + suffix + "\' in start time \'" + startTime + "\'");
				return;
			}
				
		} catch(NumberFormatException e){
			System.out.println(e.getMessage());
			return;
		}
	}
	public void setEndTime(String endTime) { //Format: hh:mmxm
		String[] time = endTime.split(":");
		if(time.length != 2 
				|| (time[0].length() != 2 && time[0].length() != 1) 
				|| time[1].length() != 4){
			System.out.println("End Time Not Set: Invalid number of digits in "+endTime);
			return;
		}
		try{
			endHour = Integer.parseInt(time[0]);
			endMinutes = Integer.parseInt(time[1].substring(0, 2));
			String suffix = time[1].substring(2,4);
			if( suffix.equalsIgnoreCase("am"))
				endsBeforeNoon = true;
			else if( suffix.equalsIgnoreCase("pm"))
				endsBeforeNoon = false;
			else{
				System.out.println("Invalid suffix \'" + suffix + "\' in end time \'" + endTime + "\'");
				return;
			}
				
		} catch(NumberFormatException e){
			System.out.println(e.getMessage());
			return;
		}
	}
	public void setDate(String aDate) { //Format: mm/dd/yyyy
		String[] date = aDate.split("/");
		if(date.length != 3 || date[0].length() != 2 || date[1].length() != 2 || date[2].length() != 4){
			System.out.println("Invalid date format: "+aDate);
			return;
		}
		try{
			month = Integer.parseInt(date[0]);
			day = Integer.parseInt(date[1]);
			year = Integer.parseInt(date[2]);
		} catch(NumberFormatException e){
			System.out.println(e.getMessage());
		}
	}
	public void setAllDay(boolean isAllDay) {
		this.isAllDay = isAllDay;
	}
	public void setLocation(String location) {
		this.location = location;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	
	//Functions
	public String toString(){
		String event = name;
		event += (" on "+ this.getDate());
		if(isAllDay)
			event += " all day";
		else{
			event += (" from " + this.getStartTime());
			event += ("-" + this.getEndTime());
		}
		event += (" at " + this.getLocation());
		return event;
	}
	//Get the Formated Start Time
	public String getStartTime() {
		if(isAllDay)
			return "12:00am";
		String st = startHour + ":";
		if(startMinutes > 9 )
			st+=startMinutes + " ";
		else
			st+= "0"+startMinutes;
		if(startBeforeNoon){
			st += "am";
		}
		else{
			st += "pm";
		}
		return st;
	}
	//Get the Formated end time
	public String getEndTime() {
		if(isAllDay)
			return "11:59pm";
		String et = endHour + ":";
		if(endMinutes > 9)
			et+= endMinutes + " ";
		else
			et += "0"+endMinutes;
		if(endsBeforeNoon){
			et += "am";
		}
		else{
			et += "pm";
		}
		return et;
	}
	//Get the formated date
	public String getDate() {
		return month + "/" + day + "/" + year;
	}
}
