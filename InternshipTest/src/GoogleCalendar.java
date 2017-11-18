/*
 * @Author: A. Danielle Talley
 * @Last Modification: 24th April 2016
 * 
 * This class implements all of the features specific
 * to using Google Calendar.
 */

import java.util.*;
import org.openqa.selenium.*;


public class GoogleCalendar {
	//Constant Variables
	private final String GOOGLECALENDARURL = "https://calendar.google.com/";
	private Map<Integer,String> FIELDNAMES;
	//Mallable Variables
	private WebDriver driver;
	private SeleniumHelper helper;
	private int maxLoginAttempts = 3;
	private Event currentEvent;
	
	
	//Constructors
	public GoogleCalendar(boolean useChrome){
		helper = new SeleniumHelper(useChrome);
		driver = helper.getDriver();
		setupMap();
	}
	public GoogleCalendar(boolean useChrome, int loginAttempts){
		helper = new SeleniumHelper(useChrome);
		driver = helper.getDriver();
		maxLoginAttempts = loginAttempts;
		setupMap();
	}
	
	//Getters
	public WebDriver getDriver() {
		return driver;
	}
	public int getMaxLoginAttempts() {
		return maxLoginAttempts;
	}
	public Event getCurrentEvent() {
		return currentEvent;
	}
	//Setters
	public void setDriver(WebDriver driver) {
		this.driver = driver;
	}
	public void setMaxLoginAttempts(int maxLoginAttempts) {
		this.maxLoginAttempts = maxLoginAttempts;
	}
	public void setCurrentEvent(Event currentEvent) {
		this.currentEvent = currentEvent;
	}
	//Initialization Function
	private void setupMap(){
		FIELDNAMES = new HashMap();
		FIELDNAMES.put(3, "name");
		FIELDNAMES.put(4, "startDate");
		FIELDNAMES.put(5, "startTime");
		FIELDNAMES.put(6, "endTime");
		FIELDNAMES.put(7, "endDate");
		FIELDNAMES.put(8, "allDay");
		FIELDNAMES.put(14, "location");
	}
	
	//Other Functions
	//This function will log in the user. 
	//The user must provide their user name and password
	public boolean LogIn(){
		WebElement current;
		boolean cont = false;
		int loginAttempts = 0;
		Scanner keyboard = new Scanner(System.in);
		//WebDriver ie = new InternetExplorerDriver();
		while(!cont && loginAttempts < maxLoginAttempts){
			driver.get(GOOGLECALENDARURL);
			
			System.out.println("Enter your UserName");
			String user = keyboard.nextLine();
			current = driver.findElement(By.cssSelector(helper.getEMAILCSS()));
			current.sendKeys(user);
			current.submit();
			try{
				helper.waitURL("password");
				System.out.println("Enter your Password");
				String pword = keyboard.nextLine();
				current = driver.findElement(By.cssSelector(helper.getPWORDCSS()));
				current.sendKeys(pword);
				current.submit();
				try{
					helper.waitURL("render");
					cont = true;
					
				} catch(TimeoutException te){
					System.out.println("Invalid Username or Password");
					loginAttempts++;
				}
			} catch(TimeoutException te){
				System.out.println("Username Not Recognized");
				loginAttempts++;
				
			}
			if(!(loginAttempts < maxLoginAttempts)){
				System.out.println("Max Number of Logins Exceeded");
				helper.endTesting(true);
				return false;
			}
		}//EndLoginWhile
		System.out.println("Log-In Successful");
		return true;
	}
	//This function will log in the user. 
	//It will use the given username and password
	public boolean LogIn(String userName, String passWord){
		WebElement current;
		boolean cont = false;
		int loginAttempts = 0;
		Scanner keyboard = new Scanner(System.in);
		//WebDriver ie = new InternetExplorerDriver();
		while(!cont && loginAttempts < maxLoginAttempts){
			driver.get(GOOGLECALENDARURL);
			
			System.out.println("Enter your UserName");
			//String user = keyboard.nextLine();
			System.out.println("User: " + userName);
			current = driver.findElement(By.cssSelector(helper.getEMAILCSS()));
			current.sendKeys(userName);
			current.submit();
			try{
				helper.waitURL("password");
				System.out.println("Enter your Password");
				//String pword = keyboard.nextLine();
				System.out.println("Password: " + passWord);
				current = driver.findElement(By.cssSelector(helper.getPWORDCSS()));
				current.sendKeys(passWord);
				current.submit();
				try{
					helper.waitURL("render");
					cont = true;
					
				} catch(TimeoutException te){
					System.out.println("Invalid Username or Password");
					loginAttempts++;
				}
			} catch(TimeoutException te){
				System.out.println("Username Not Recognized");
				loginAttempts++;
				
			}
			if(!(loginAttempts < maxLoginAttempts)){
				System.out.println("Max Number of Logins Exceeded");
				helper.endTesting(true);
				return false;
			}
		}//EndLoginWhile
		System.out.println("Log-In Successful");
		return true;
	}
	//This function will create an event using the "quick event" option on the main screen.
	//It will use the 'currentEvent' as the target Event
	public boolean createQuickEvent(){//Event event){
		if(currentEvent == null){
			System.out.println("No event available");
			return false;
		}
		//Make sure we're on the right screen and logged in
		if(!isLoggedIn())
			return false;
		quickAdd();
		System.out.println("Event Created Successfully");
		return true;
		
	}
	//This function will create an event using the "quick event" option on the main screen.
	//It will use the given event as the target Event and set 'currentEvent'
	public boolean createQuickEvent(Event event){//Event event){
		currentEvent = event;
		//Make sure we're on the right screen and logged in
		if(!isLoggedIn())
			return false;
		quickAdd();
		System.out.println("Event Created Successfully");
		return true;
		
	}
	//This will use the "Create" button on the main screen to create an event
	//It will use the 'currentEvent' as the target event
	public void createEvent(){
		if(!isLoggedIn())
			return;
		WebElement createPanel = driver.findElement(By.className("qnb-container"));
		List<WebElement> createChildren = createPanel.findElements(By.cssSelector("*"));
		for(WebElement we : createChildren){
			if(we.getText().equals("CREATE")){
				we.click();
				try{
					helper.waitURL("event");
				}catch(TimeoutException e){
					System.out.println(e.getMessage());
				}
				break;
			}
		}
		List<WebElement> fields = driver.findElements(By.xpath("//input[@*]"));
		//helper.printElements(fields);
		for(WebElement current : fields){
			if(FIELDNAMES.containsKey(current.getAttribute("id"))){
				//System.out.println("SWITCH ON: "+current.getAttribute("id"));
				switch(FIELDNAMES.get(current.getAttribute("id"))){
					case("name"):
						selectAndFill(current, currentEvent.getName());
						break;
					case("startDate"):
						selectAndFill(current, currentEvent.getDate());
						break;
					case("startTime"):
						selectAndFill(current, currentEvent.getStartTime());
						break;
					case("endTime"):
						selectAndFill(current, currentEvent.getEndTime());
						break;
					case("endDate"):
						//selectAndFill(current, currentEvent.getEndDate()); //NotImplemented
						break;
					case("allDay"):
						if(currentEvent.isAllDay()){
							current.click();
						}
						break;
					case("location"):
						selectAndFill(current, currentEvent.getLocation());
						break;
					default:
						System.out.println("ERROR: CASE NOT FOUND FOR: " + current.getAttribute("id"));
				}
			}
		}
		driver.findElement(By.id(":1t.save_top")).click();
		helper.waitURL("render");
		System.out.println("Event created successfully in Google Calendar");
	}
	//This will use the "Create" button on the main screen to create an event
	//It will use the given event as the target event and update the 'currentEvent'
	public void createEvent(Event event){
		currentEvent = event;
		if(!isLoggedIn())
			return;
		System.out.println("Finding Create Button");
		WebElement createPanel = driver.findElement(By.className("qnb-container"));
		List<WebElement> createChildren = createPanel.findElements(By.cssSelector("*"));
		for(WebElement we : createChildren){
			if(we.getText().equals("CREATE")){
				we.click();
				try{
					helper.waitURL("event");
				}catch(TimeoutException e){
					System.out.println(e.getMessage());
				}
				break;
			}
		}
		System.out.println("Getting All Input Fields");
		List<WebElement> fields = driver.findElements(By.xpath("//input[@*]"));
		//helper.printElements(fields);
		System.out.println("Filling Out Input Fields");
		for(int i = 0 ; i < fields.size(); i++){
			if(FIELDNAMES.containsKey(i)){
				WebElement current = fields.get(i);
				//System.out.println("SWITCH ON: "+current.getAttribute("id"));
				switch(FIELDNAMES.get(i)){
					case("name"):
						selectAndFill(current, currentEvent.getName());
						break;
					case("startDate"):
						selectAndFill(current, currentEvent.getDate());
						break;
					case("startTime"):
						selectAndFill(current, currentEvent.getStartTime());
						break;
					case("endTime"):
						selectAndFill(current, currentEvent.getEndTime());
						break;
					case("endDate"):
						//selectAndFill(current, currentEvent.getEndDate()); //NotImplemented
						break;
					case("allDay"):
						if(currentEvent.isAllDay()){
							current.click();
						}
						break;
					case("location"):
						selectAndFill(current, currentEvent.getLocation());
						break;
					default:
						System.out.println("ERROR: CASE NOT FOUND FOR: " + current.getAttribute("id"));
				}
			}
		}
		System.out.println("Saving");
		driver.findElement(By.cssSelector("[id*=save_top]")).click();
		helper.waitURL("render");
		System.out.println("Event created successfully in Google Calendar");
	}
	
	//This will close current session
	//if closeBrowser = true, the browser window will also close
	public void endSession(boolean closeBrowser){
		helper.endTesting(closeBrowser);
	}

	//private functions
	private void selectAndFill(WebElement we, String input){
		we.click();
		we.clear();
		we.sendKeys(input);
	}
	private void quickAdd(){
		System.out.println("Quick Adding Event");
		WebElement quickAdd = driver.findElement(By.className("qnb-container"));
		quickAdd.click();
		WebElement eventInfo= driver.switchTo().activeElement();
		eventInfo.click();
		eventInfo.sendKeys(currentEvent.toString());
		eventInfo.sendKeys(Keys.RETURN);
		
	}
	private boolean isOnMainScreen(){
		if(driver.getCurrentUrl().contains("main"))
			return true;
		else
			return false;
	}
	private boolean isLoggedIn(){
		if(!isOnMainScreen()){
			driver.get(GOOGLECALENDARURL);
			if(!isOnMainScreen())
				if(!LogIn()){
					System.out.println("Cannot Create an Event: Login Unsuccessful");
					return false;
				}
		}
		return true;
	}
}
