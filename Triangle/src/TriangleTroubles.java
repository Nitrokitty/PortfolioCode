import java.applet.*;
import java.awt.*; 
import java.util.*;

public class TriangleTroubles extends Applet{
	//variables
	private Image window;
	private Graphics area;
	
	//initialize window and draw the triangles
	public void init()
	{
		int height = getSize().height; //get the height
		int width = getSize().width; //get the width
		window = createImage(width,height); //create the window
		area = window.getGraphics(); ///setting it up to draw
		drawBaseTriangle(area, height, width); //drawing the base triangle (the one that's right side up)
		drawWindow(area, 0, 0, height, width); //drawing the other triangles
	}
	//drawing the end image
	public void paint(Graphics g)
	{
		g.drawImage(window,0,0,null); 
	}
	
	//this will draw the first triangle
	public static void drawBaseTriangle(Graphics g, int height, int width)
	{
		//creating the array of the points of the triangle { left point, middle point, right point}
		int [] x = {0, width/2, width};
		int [] y = {height, 0, height};
		g.setColor(Color.black);
		g.fillPolygon(x, y, 3);
	}
	
	/*
	 * This method will first draw an up-side-down triangle (see drawTriangle). 
	 * Then, it will create three theoretical windows where the next triangles 
	 * will be drawn. One window will be the bottom left triangle, the next will
	 * be the center top triangle, and the last will be the bottom right triangle. 
	 * Then the same triangle is drawn in each window. Finally, three more windows
	 * are called within each window until either the width or height are less than
	 * 4 pixels. See the "Methodology" file.
	 */
	public static void drawWindow(Graphics g, int wS, int hS, int hE, int wE)
	//wS = width start, hS = height start, hE = height end, wE = width end
	{
		if((hE-hS) < 4 || (wE-wS) < 4) //if the width or height is less than 4 pixels
		{
			return; //stop drawing
		}
		else
		{
			drawTriangle(g, wS, hS, hE, wE); //draw the triangle in the current window
			//creating the three new windows within the current window... just so I can see it better
			int [] windowA = { wS, (hE+hS)/2, hE, (wE-wS)/2 + wS }; //bottom left window
			int [] windowB = { ((wE-wS)/4)+wS, hS, (hE+hS)/2, wE-((wE-wS)/4)}; //center top window
			int [] windowC = { (wE+wS)/2, (hE+hS)/2, hE, wE}; //bottom right window
			//drawing the three new windows
			drawWindow(g, windowA[0], windowA[1], windowA[2], windowA[3]);
			drawWindow(g, windowB[0], windowB[1], windowB[2], windowB[3]);
			drawWindow(g, windowC[0], windowC[1], windowC[2], windowC[3]);
		}
	}
	//this will draw the only triangle needed within each window
	private static void drawTriangle(Graphics g, int wS, int hS, int hE, int wE)
	//wS = width start, hS = height start, hE = height end, wE = width end
	{
		//creating the array of the points of the triangle { left point, middle point, right point}
		int [] x = { ((wE-wS)/4)+wS, ((wE-wS)/2)+wS, (3*(wE-wS)/4)+wS};
		int [] y = { ((hE-hS)/2)+hS, (hE), ((hE-hS)/2)+hS};
		g.setColor(Color.blue);
		g.fillPolygon(x, y, 3);
	}

}