
public class testDriver {
	public static void main(String[] args) {
		binaryTree BST = new binaryTree(10);
		
		System.out.println("Welcome to the biggest organizing pain... .ever.... ");
		
		int [] numberArray = {11, 4, 2, 7, 16, 3, 14, 0, 9, 20, 15, 8, 12, 13, -1, -30, 5};
		for(int i = 0; i < numberArray.length; i++)
		{
			BST.insert(numberArray[i]);
		}

		BST.delete(9);
		BST.writeOutput();


	}

}
