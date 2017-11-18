/*
 * Sprout: R&B Tree Creator
 * Created by Audrey "Danielle" Talley
 * 18 March 2015
 * (Helper Class)
 * This is the Node class. It will set up nodes. It has
 * the parameters data, left child node, right 
 * child node, and color. For color, black = false and
 * red = true.
 */
public class Node <T extends Comparable<T>> {
	//variables
	private T data;
	private Node left;
	private Node right;
	private boolean color; //black = 0 & red = true
	
	//Initializers
	public Node()
	{
		this.color = false;
		this.data = null;
		this.left = null;
		this.right = null;
	}
	
	public Node(T someData, boolean aColor)
	{
		this.data = someData;
		this.color = aColor;
		this.left = null;
		this.right = null;
	}
	
	public Node(T someData, boolean aColor, Node leftNode, Node rightNode)
	{
		this.data = someData;
		this.color = aColor;
		this.left = leftNode;
		this.right = rightNode;
	}

	
	//Accessors & Mutators
	public T getData() {
		return data;
	}

	public void setData(T data) {
		this.data = data;
	}

	public Node getLeft() {
		return left;
	}

	public void setLeft(Node left) {
		this.left = left;
	}

	public Node getRight() {
		return right;
	}

	public void setRight(Node right) {
		this.right = right;
	}

	public boolean isColor() {
		return color;
	}

	public void setColor(boolean color) {
		this.color = color;
	}	
}
