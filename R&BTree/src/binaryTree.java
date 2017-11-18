/*
 * Sprout: R&B Tree Creator
 * Created by Audrey "Danielle" Talley
 * 18 March 2015
 * (Helper Class)
 * This is the main tree class. It will traverse nodes to create a tree.
 * The root is a the top node and the root will always start black. 
 * It has 3 main functions: insert, delete, and print.
 */


public class binaryTree <T extends Comparable<T>> {
	private Node root;
	private boolean alternate;
	private static boolean RED = true;
	private static boolean BLACK = false;
	
	//Initializations
	public binaryTree()
	{
		root = new Node();
	}
	
	public binaryTree(T data)
	{
		//root will always starts BLACK
		root = new Node(data, BLACK, new Node(null, BLACK), new Node(null, BLACK));
		alternate = false;
	}
	
	
	
	//insert data
	public void insert(T data)
	{
		if(root == null)
		{
			root = new Node(data, BLACK, new Node(null, BLACK), new Node(null, BLACK));
		}
		else
		{
			searchAndInsert(root, data);
		}
	}
	
	//print the output
	public void writeOutput()
	{
		print(root, 0, "");
	}
	
	//delete a node
	public void delete(T data)
	{
		if(findNode(root, data) != null)
		{
			searchAndDelete(root, data);
		}
		else
		{
			System.out.println(data+" is not in this tree");
		}
		
	}
	
	
	//this will start a new tree
	public void clearAll()
	{
		root = new Node();
	}
	
	//main insert helper function
	private void searchAndInsert(Node someNode, T iData)
	{
		//Node tempNode = null;
		if(someNode.getData() == null)
		{
			someNode.setData(iData);
			someNode.setColor(RED);
			someNode.setLeft(new Node(null, BLACK));
			someNode.setRight(new Node(null, BLACK));
			insertion1(someNode);
			return;
		}
		if( someNode.getData().compareTo(iData) > 0) //if data to be inserted is less than the node
		{
			searchAndInsert(someNode.getLeft(), iData);
		}
		else if( someNode.getData().compareTo(iData) < 0)
		{
			searchAndInsert(someNode.getRight(), iData);
		}
		else
		{
			System.out.println("Can not insert duplicate data");
			return;
		}
		
		//someNode.setColor(checkColors(someNode));
		//System.out.println(someNode.getData());
		return;
	}
	
	//main delete helper function
	private void searchAndDelete(Node aNode, T dData)
	{
		if(aNode.getData() == null)
		{
			System.out.println("There is no root.");
			return;
		}
		Node node = findNode(aNode, dData);
		if(node == null)
		{
			return;
		}
		//data found
		else
		{
			//if the node is RED then atleast one of it's two nodes are leaves
			
			if(node.isColor() == RED || node == root)
			{
				//in order to more accurately select a branch to choose from
				//it will chose either the max or min based on runtime
				//since the functions are almost identical it is safe to assume
				//that the longer the run time, the longer the branch
				//so we want to choose the longest branch
				long maxTime = System.nanoTime();
				max(node, false);
				maxTime = System.nanoTime() - maxTime;
				long minTime = System.nanoTime();
				min(node, false);
				minTime = System.nanoTime() - minTime;
				//System.out.println(maxTime +"\t"+ minTime);
				if(maxTime > minTime)
				{
					max(node, true);
				}
				else
				{
					min(node, false);
				}
				
			}
			
			//if one of the child nodes are RED
			else if(node.getLeft().isColor()==RED || node.getRight().isColor()==RED)
			{
				if(node.getRight().isColor() == RED)  
				{
					min(node, true);
				}
				else
				{
					max(node, true);
				}
				node.setColor(BLACK);
			}
			else
			{
				Node parent = findParent(node);
				Node sibl = findSecondary(parent, node);
				node.setRight(null);
				node.setLeft(null);	
				node.setData(null);
				node.setColor(BLACK);
				if(parent != null && parent.getLeft() == node)
				{
					node = parent.getLeft();
				}
				else if(parent != null)
				{
					node = parent.getRight();
				}
				
				//writeTest(parent);
				
				deletion1(node, parent, sibl);
				
			}
		}//end data found*/
	}//end function
	
	//printing helper
	private void print(Node currNode, int level, String path)
	{
		//System.out.println();
		if(level == 0)
		{
			System.out.println("Path = direction from root, R= right, L=left, Level = number of nodes away from root");
			System.out.println();
			System.out.println("Data\tColor\tPath\tLevel");
		}
		if(currNode.getData()!=null)
		{
			//System.out.println(level);
			System.out.print(currNode.getData()+"\t");
			if(currNode.isColor())
			{
				System.out.print("RED\t");
			}
			else
			{
				System.out.print("BLACK\t");
			}
			if(path == "")
			{
				System.out.print("root\t");
			}
			else
			{
				System.out.print(path+"\t");
			}
			System.out.println(level);
			level++;
			print(currNode.getLeft(), level, path+"L ");
			print(currNode.getRight(), level, path+"R ");
		}
	}
	
	
	//soo much insertion help
	private void insertion1(Node node)
	{
		Node parent = findParent(node);
		if(parent == null)
		{
			node.setColor(BLACK);
		}
		else
		{
			insertion2(node);
		}
	}
	private void insertion2(Node node)
	{
		Node parent = findParent(node);
		if(parent.isColor() == BLACK)
		{
			return;
		}
		insertion3(node);
	}
	private void insertion3(Node node)
	{
		Node parent = findParent(node);
		Node gparent = findParent(parent);
		Node uncle;
		if(gparent.getLeft() == parent)
		{
			uncle = gparent.getRight();
		}
		else
		{
			uncle = gparent.getLeft();
		}
		if( uncle != null && uncle.isColor() == RED && parent!=null && parent.isColor() == RED)
		{
			parent.setColor(BLACK);
			uncle.setColor(BLACK);
			gparent.setColor(RED);
			insertion1(gparent);
		}
		else
		{
			insertion4(node);
		}
	}
	private void insertion4(Node node)
	{
		Node parent = findParent(node);
		Node gparent = findParent(parent);
		Node uncle;
		if(gparent.getLeft() == parent)
		{
			uncle = gparent.getRight();
		}
		else
		{
			uncle = gparent.getLeft();
		}
		if(parent.isColor() == RED && uncle.isColor() == BLACK)
		{
			if(parent.getRight() == node && gparent.getLeft() == parent)
			{
				rotateLeft(parent);
			}
			else if(parent.getLeft() == node && gparent.getRight() == parent)
			{
				rotateRight(parent);
			}
		}
		insertion5(node);
	}
	
	private void insertion5(Node node)
	{
		Node parent = findParent(node);
		Node gparent = findParent(parent);
		Node uncle;
		if(gparent.getLeft() == parent)
		{
			uncle = gparent.getRight();
		}
		else
		{
			uncle = gparent.getLeft();
		}
		
		
		if(parent.isColor() == RED && uncle.isColor() == BLACK)
		{
			if(parent.getLeft() == node && gparent.getLeft() == parent)
			{
				rotateRight(gparent);
				boolean PC = parent.isColor();
				parent.setColor(gparent.isColor());
				gparent.setColor(PC);
			}
			else if(parent.getRight() == node && gparent.getRight() == parent)
			{
				rotateLeft(gparent);
				boolean PC = parent.isColor();
				parent.setColor(gparent.isColor());
				gparent.setColor(PC);
			}
		}
	}

	
	//rotation helpers
	private void rotateRight(Node R)
	{
		//System.out.println("Right " + R.getData());
		Node Rcopy = R;
		Node RR = R.getRight();
		Node RL = R.getLeft();
		Node RRR = RR.getRight();
		Node RRL = RR.getLeft();
		
		//invert tree
		R.setLeft(RR);
		R.setRight(RL);
		
		
		//switch the data... doing this will preserve connections
		boolean GC = R.isColor(); 
		T GD = (T) R.getData();
		R.setData(RL.getData());
		R.setColor(RL.isColor());
		RL.setColor(GC);
		RL.setData(GD);
		
		//invert nodes
		Node RLL = RL.getLeft();
		RL.setLeft(RL.getRight());
		RL.setRight(RLL);
		
		
		//switch ends
		RL.setRight(RR);
		R.setLeft(RLL);
	}	
	private void rotateLeft(Node R)
	{
		Node Rcopy = R;
		Node RR = R.getRight();
		Node RL = R.getLeft();
		Node RRR = RR.getRight();
		Node RRL = RR.getLeft();
		
		//invert tree
		R.setLeft(RR);
		R.setRight(RL);
		
		//switch Data
		boolean GC = R.isColor(); 
		T GD = (T) R.getData();
		R.setData(RR.getData());
		R.setColor(RR.isColor());
		RR.setColor(GC);
		RR.setData(GD);
		
		//switch nodes
		RR.setLeft(RRR);
		RR.setRight(RRL);
		
		
		//switch nodes (ends)
		R.getLeft().setLeft((R.getRight()));
		R.setRight(RRR);
		R.getLeft().setRight(RRL);

	}
	
	
	//finding node assister
	private Node findNode(Node aNode, T data)
	{
		if(aNode.getData() == null)
		{
			//System.out.println("Data not found");
			return null;
		}
		else if(aNode.getData().compareTo(data) > 0)
		{
			return findNode(aNode.getLeft(), data);
		}
		else if(aNode.getData().compareTo(data) < 0)
		{
			return findNode(aNode.getRight(), data);
		}
		else
		{
			return aNode;
		}
	}
	
	//find siling of a node
	private Node findSecondary(Node parent, Node node)
	{
		if(parent != null)
		{
			if(parent.getLeft() == node)
			{
				return parent.getRight();
			}
			else
			{
				return parent.getLeft();
			}
		}
		else
		{
			return null;
		}
	}
	
	//find the parent of a node
	private Node findParent(Node aNode)
	{
		//System.out.println(aNode.getData());
		if(aNode != root)
		{
			boolean toContinue = true;
			Node parent = root;
			while(toContinue)
			{
				if(parent.getLeft() == aNode || parent.getRight() == aNode)
				{
					toContinue = false;
					break;
				}
				else if(parent.getData().compareTo(aNode.getData()) > 0)
				{
					parent = parent.getLeft();
				}
				else if(parent.getData().compareTo(aNode.getData()) < 0)
				{
					parent = parent.getRight();	
				}
			}
			return parent;
		}
		else
		{
			return null;
		}
	}
	
	//find the uncle of a node
	private Node findUncle(Node grandPNode, Node PNode)
	{
		if(grandPNode!=null)
		{
			if(grandPNode.getRight() == PNode)
			{
				return grandPNode.getLeft();
			}
			else
			{
				return grandPNode.getRight();
			}
		}
	else
	{
		return null;
	}
		
	}
	

	
	//soo much deletion help
	private void deletion1(Node primary1, Node parent, Node sibl)
	{
		if(parent != null)
		{
			deletion2(primary1, parent, sibl);
		}
		else
		{
			primary1.setColor(BLACK);
		}
	}
	private void deletion2(Node node, Node parent, Node sibl)
	{
		if(sibl.isColor() == RED)
		{
			//flip these two colors
			boolean newColor = parent.isColor();
			parent.setColor(sibl.isColor());
			sibl.setColor(newColor);
			
			if(parent.getLeft() == node)
			{
				rotateLeft(parent);
			}
			else
			{
				rotateRight(parent);
			}
		}
		deletion3(node, parent, sibl);
	}
	private void deletion3(Node node, Node parent, Node sibl)
	{
		if(parent.isColor() == BLACK && sibl.isColor() == BLACK && sibl.getLeft().isColor() == BLACK && sibl.getRight().isColor() == BLACK)
		{
			sibl.setColor(RED);
			deletion1(parent, findParent(parent), findSecondary(findParent(parent), parent ));
		}
		else
		{
			deletion4(node, parent, sibl);
		}
	}
	private void deletion4(Node node, Node parent, Node sibl)
	{
		if(parent.isColor() == RED && sibl.isColor() == BLACK && sibl.getLeft().isColor() == BLACK && sibl.getRight().isColor() == BLACK)
		{
			parent.setColor(!parent.isColor());
			sibl.setColor(!sibl.isColor());
		}
		else
		{
			deletion5(node, parent, sibl);
		}
		
	}
	private void deletion5(Node node, Node parent, Node sibl)
	{
		if(sibl.isColor() == BLACK)
		{
			if(parent.getLeft() == node && sibl.getLeft().isColor() == RED && sibl.getRight().isColor() == BLACK)
			{
				sibl.setColor(RED);
				sibl.getLeft().setColor(BLACK);
				rotateRight(sibl);
			}
			else if(parent.getRight() == node && sibl.getLeft().isColor() == BLACK && sibl.getRight().isColor() == RED)
			{
				sibl.setColor(RED);
				sibl.getRight().setColor(BLACK);
				rotateLeft(sibl);
			}
		}
		deletion6(node, parent, sibl);
	}
	
	private void deletion6(Node node, Node parent, Node sibl)
	{		
		boolean newPColor = parent.isColor();
		parent.setColor(BLACK);
		sibl.setColor(newPColor);
		if(parent.getLeft() == node)
		{
			sibl.getRight().setColor(BLACK);
			rotateLeft(parent);
		}
		else
		{
			sibl.getLeft().setColor(BLACK);
			rotateRight(parent);
		}
	}
	
	
	
	
	
	//find the maximum of subsuquent nodes from given node
	private void max(Node aNode, boolean setNode)
	{
		//writeTest(aNode);
		Node searchBranch = aNode.getLeft();
		if(searchBranch.getRight() != null)
		{
			while(searchBranch.getRight().getData()!=null)
			{
				searchBranch = searchBranch.getRight();
			}
		}
		if(setNode)
		{
			setNodeFromMaxOrMin(searchBranch, aNode);
		}

		//writeTest(aNode);
	}
	//find minimum of subusquent nodes from start node
	private void min(Node aNode, boolean setNode)
	{
		//writeTest(aNode);
		Node searchBranch = aNode.getRight();
		if(searchBranch.getLeft() != null)
		{
			while(searchBranch.getLeft().getData()!=null)
			{
				searchBranch = searchBranch.getLeft();
			}
		}
		if(setNode)
		{
			setNodeFromMaxOrMin(searchBranch, aNode);
		}
		//writeTest(aNode);
	}
	
	private void setNodeFromMaxOrMin(Node searchBranch, Node aNode)
	{
		Node parentS;
		if(aNode.getLeft() == searchBranch || aNode.getRight() == searchBranch)
		{
			parentS = aNode;
		}
		else
		{
			parentS = findParent(searchBranch);
		}
		if(parentS.getLeft() == searchBranch)
		{
			parentS.setLeft(new Node(null, BLACK));
		}
		else
		{
			parentS.setRight(new Node(null, BLACK));
		}
		aNode.setData(searchBranch.getData());
		aNode.setColor(searchBranch.isColor());
	}
	
	//this will just cycle through one branch
	//I had to do this instead of just timing how long max & min took to run because I set the nodes within the max & min
	//in retrospect i should have probably just altered those functions
	private int findEndOfBranch(Node node, boolean goRight, int level)
	{
		if(goRight)
		{
			if(node.getRight().getData() != null)
			{
				level++;
				level = findEndOfBranch(node.getRight(), goRight, level);
			}
			else
			{
				return level;
			}
			
		}
		else
		{
			if(node.getLeft().getData() != null)
			{
				level++;
				level = findEndOfBranch(node.getLeft(), goRight, level);
			}
			else
			{
				return level;
			}
		}
		return level;
	}
	
	
	
	
	//used for testing only
	private void writeTest(Node R)
	{
		System.out.print("Root: "+R.getData());
		System.out.print("\tRight: "+R.getRight().getData());
		if(R.getRight().getLeft()!= null)
		{
			System.out.print("\tRL: "+R.getRight().getLeft().getData());
		}
		if(R.getRight().getRight()!= null)
		{
			System.out.print("\tRR: "+R.getRight().getRight().getData());
		}
		System.out.print("\tLeft: "+R.getLeft().getData());
		if(R.getLeft().getLeft()!= null)
		{
			System.out.print("\tLL: "+R.getLeft().getLeft().getData());
		}
		if(R.getLeft().getRight()!= null)
		{
			System.out.print("\tLR: "+R.getLeft().getRight().getData());
		}
		System.out.println();
	}
}
