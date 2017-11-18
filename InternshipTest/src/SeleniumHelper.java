/*
 * @Author: A. Danielle Talley
 * @Last Modification: 24th April 2016
 * 
 * This class is a helper class for
 * generic Selenium features
 */
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.WebDriverWait;


public class SeleniumHelper {
	
	//Constant Variables
	private static final String DRIVER_PATH = "src\\Drivers\\";
	private static final String CHROME_DRIVER = "chromedriver.exe";
	private static final String IE_DRIVER = "IEDriverServer.exe";
	private static final String ERROR_CSS = "error-msg";
	private static final String EMAILCSS = "input[type='email']";
	private static final String PWORDCSS = "input[type='password']";
	//Mallable Variables
	private WebDriver driver;
	private int maxTimeOut = 10;
	
	//Constructors
	public SeleniumHelper(boolean useChrome){
		setupDrivers();
		if(useChrome)
			driver = new ChromeDriver();
		else
			driver = new InternetExplorerDriver();
	}
	
	public SeleniumHelper(boolean useChrome, int maxTimeOut){
		setupDrivers();
		if(useChrome)
			driver = new ChromeDriver();
		else
			driver = new InternetExplorerDriver();
		this.maxTimeOut = maxTimeOut;
	}
	
	private void setupDrivers(){
		System.setProperty("webdriver.chrome.driver", DRIVER_PATH + CHROME_DRIVER);
		System.setProperty("webdriver.ie.driver", DRIVER_PATH + IE_DRIVER);
	}
	
	//Getters
	public WebDriver getDriver(){
		return this.driver;
	}
	public int getMaxTimeOut() {
		return maxTimeOut;
	}
	public static String getERROR_CSS() {
		return ERROR_CSS;
	}
	public static String getEMAILCSS() {
		return EMAILCSS;
	}

	public static String getPWORDCSS() {
		return PWORDCSS;
	}
	//Setters
	public void setMaxTimeOut(int aMaxTimeOut) {
		maxTimeOut = aMaxTimeOut;
	}
	
	//Functions
	//First Test Ever
		public void superEasyTest(){
			driver.get("https://www.google.com/");
			WebElement searchBar = driver.findElement(By.name("q"));
			searchBar.sendKeys("this is super cool");
			searchBar.submit();
			waitTitle("this is super cool");
			System.out.println("Page title: "+driver.getTitle());
		}
	//This function will wait until the given title (text) is displayed
	public void waitTitle(String text){
		System.out.println("Waiting");
		(new WebDriverWait(driver, maxTimeOut)).until(new ExpectedCondition<Boolean>(){
			public Boolean apply(WebDriver d){
				return d.getTitle().toLowerCase().startsWith(text);
			}
		});
		System.out.println("End Wait");
	}
	//This function will wait until the given URL (text) is displayed
	public void waitURL(String text) throws TimeoutException{
		System.out.println("Waiting");
		(new WebDriverWait(driver, maxTimeOut)).until(new ExpectedCondition<Boolean>(){
			public Boolean apply(WebDriver d){
				return d.getCurrentUrl().contains(text);
			}
		});
		System.out.println("End Wait");
	}
	//This function will wait until the given URL (currentURL) changes
	public void waitURLChange(String currentURL) throws TimeoutException{
		System.out.println("Waiting");
		(new WebDriverWait(driver, maxTimeOut)).until(new ExpectedCondition<Boolean>(){
			public Boolean apply(WebDriver d){
				return !d.getCurrentUrl().contains(currentURL);
			}
		});
		System.out.println("End Wait");
	}
	//This will print the Tag, ID, Class, and Text of all the web elements in a list
	public void printElements(List<WebElement> list){
		System.out.println("TAG\tID\tCLASS\tTEXT");
		for(WebElement e: list){
			System.out.println(e.getTagName()+"\t"+e.getAttribute("id")+"\t"+e.getClass()+"\t"+e.getText());
			
		}
	}
	//This will print some information about a web element
	public void printElement(WebElement we){
		System.out.println(we.getTagName()+"\t"+we.getAttribute("id")+"\t"+we.getClass()+"\t"+we.getText());
	}
	//This will end the test by possibly closing the driver and exiting eclipse
	public void endTesting(boolean closeBrowser){
		System.out.println("Ending Testing");
		if(closeBrowser)
			driver.quit();
		System.exit(0);
	}
	
/*	Used for testing
 * public void makeDictionary(boolean toPrint){
		System.out.println("Getting Elements");
		List<WebElement> elements = driver.findElements(By.cssSelector("*"));
		System.out.println("Num of Elements: " +elements.size());
		Map<String, Integer> tags = new HashMap<String, Integer>();
		System.out.println("Creating Dictionary");
		System.out.println("Dictionary Completion: ");
		int sum = 0;
		boolean wait = false;
		for(WebElement e: elements){
			if(tags.containsKey(e.getTagName()))
				tags.put( e.getTagName(), tags.get(e.getTagName())+1);
			else
				tags.put(e.getTagName(), 1);
			sum++;
			int completion = (int)(sum*100/(float)elements.size()); 
			if(completion > 0 && !wait && completion%10 ==0){
				System.out.print((int)(sum*100/(float)elements.size())+"%\t");
				wait = true;
			}
			else if(completion%10 == 1 && wait)
				wait = false;
		}
		if(toPrint){
			System.out.println("\nPrinting Tags");
			for(String tag: tags.keySet()){
				System.out.println("Tag: "+tag+"\tCount: "+tags.get(tag));
			}
		}
	}
	*/
}
