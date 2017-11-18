import java.util.*;
import java.util.concurrent.TimeUnit;
 




import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.events.WebDriverEventListener;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;


public class League {
	/*
	WebElement current;
	chrome.get("http://na.leagueoflegends.com/");
	
	current = chrome.findElement(By.xpath("//*[@class='link-login']"));
	current.click();
	waitURL(chrome, "auth");
	
	//List<WebElement> signInForm = chrome.findElements(By.xpath("//form[@id='login-form']"));
	//get all inputs
	List<WebElement> inputs = chrome.findElements(By.tagName("input"));
	//List<WebElement> selections = chrome.findElements(By.tagName("select"));
	for(WebElement e : inputs){
		String att = e.getAttribute("id");
		if(att.contains("user")){
			System.out.println("Enter your username");
			//e.click();
			e.sendKeys(keyboard.nextLine());
		}
		else if(att.contains("pass")){
			System.out.println("Enter your password");
			//e.click();
			e.sendKeys(keyboard.nextLine());
		}
	}
	Select regions = new Select(chrome.findElement(By.id("login-form-region")));
	boolean hasBeenSelected = false;
	while(!hasBeenSelected){
		System.out.println("Type your region number: ");
		int i = 1;
		for(WebElement e : regions.getOptions()){
			System.out.println(i+": "+e.getText());
			i++;
		}
		int selection = keyboard.nextInt();
		if(selection-1 > regions.getOptions().size())
			System.out.println("Choose the number in the available list");
		else{
			System.out.println(regions.getOptions().get(selection-1).getText());
			regions.selectByIndex(selection-1);
			hasBeenSelected = true;
		}
	}
	chrome.switchTo().activeElement().submit();*/
}
