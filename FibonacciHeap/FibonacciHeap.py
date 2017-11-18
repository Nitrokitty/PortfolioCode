import random
import math

class FibonacciHeap:
    
    trees = None
    min_tree = None
    root = None;

    def __init__(self):
        self.trees = list();
        return;

    def insert(self, value):
        if(not(type(value) == type(list()))):
            old_value = value
            value = list()
            value.append(old_value)
        for v in value:
            if(self.min_tree == None):            
                new_tree =  Tree(v);
                self.min_tree = new_tree
            else:
                new_tree = Tree(v, self.min_tree, self.min_tree.right_sibling)
                new_tree.right_sibling.left_sibling = new_tree
                self.min_tree.right_sibling = new_tree                            
                if(self.min_tree.value > new_tree.value):
                    self.min_tree = new_tree
            self.trees.append(new_tree)


    def insert_tree(self, tree):        
        if(self.min_tree == None):
            new_tree = Tree(tree.value)
            self.min_tree = tree
        else:
            new_tree = Tree(tree.value, self.min_tree, self.min_tree.right_sibling)
            new_tree.right_sibling.left_sibling = new_tree
            self.min_tree.right_sibling = new_tree            
            if(self.min_tree.value > new_tree.value):
                self.min_tree = new_tree
                
        new_tree.children = tree.children
        self.trees.append(new_tree)
        return new_tree
    
    
    
    def union(self, other_heap):
        old_right_sibling = self.min_tree.right_sibling;    
        other_heap_old_left_sibling = other_heap.min_tree.left_sibling;
        
        self.min_tree.right_sibling = other_heap.min_tree;        
        other_heap.min_tree.left_sibling = self.min_tree;
        old_right_sibling.left_sibling = other_heap_old_left_sibling
        other_heap_old_left_sibling.right_sibling = old_right_sibling                
        
        if(self.min_tree.value > other_heap.min_tree.value):
            self.min_tree = self.min_tree.right_sibling;

        curr_tree = self.min_tree;
        while True:
            if(not(curr_tree in self.trees)):
                self.trees.append(curr_tree)
            curr_tree = curr_tree.right_sibling
            if(curr_tree == self.min_tree):
                break
            

    def consolidate_trees(self, tree, degree_dict):
        already_done_tree = degree_dict.pop(tree.degree)

        if(already_done_tree.value < tree.value):
            chosen_root = already_done_tree
            chosen_child = tree
        else:
            chosen_root = tree;
            chosen_child =  already_done_tree;     

        left = chosen_child.left_sibling
        right = chosen_child.right_sibling

        left.right_sibling = right;
        right.left_sibling = left;        

        self.trees.remove(chosen_child)
        chosen_root.add_child(chosen_child)        
        
        if(chosen_root.degree in degree_dict.keys()):
            return self.consolidate_trees(chosen_root, degree_dict)
        else:
            degree_dict[chosen_root.degree] = chosen_root;
            return chosen_root

    def extract_min(self):
        old_min = self.min_tree
        
        if(not(len(old_min.children) == 0)):
            for i in range(len(old_min.children)):                
                self.insert_tree(old_min.children[i])
        
        self.trees.remove(old_min)            
        left = old_min.left_sibling
        right = old_min.right_sibling
        
        left.right_sibling = right
        right.left_sibling = left            
                
        degree_dict = dict()
       
        t = right;
        self.min_tree = t
        start = t
        while True:
            if(t.degree in degree_dict.keys() and not(degree_dict[t.degree]==t)):
                t = self.consolidate_trees(t, degree_dict)
            else:
                degree_dict[t.degree] = t

            if(t.value < self.min_tree.value):
                self.min_tree = t
            
            if(not(start in degree_dict.values())):
                start = t
                self.min_tree = t
            
            t = t.right_sibling
            if(t == start):
                break
        return old_min.value

    def find_tree(self, value):
        curr_tree = self.min_tree
        while True:
            if(curr_tree.value == value):
                 return curr_tree
            else:
                t = curr_tree.find_tree(value)
                if(not(t == None)):
                    return t
            curr_tree = curr_tree.right_sibling
            if(curr_tree == self.min_tree):
                return None
        
    
    def decrease_key(self, tree, value):
        
        tree.value -= value

        if(tree.get_is_root_tree()):
            return tree
        print("Tree: " + str(tree.value) + "\tParent: " + str(tree.parent.value))
        if(tree.value < tree.parent.value):
            tree = self.cascading_cut(tree)
        return tree


    def cascading_cut(self, tree):
        old_parent = tree.parent
        old_parent.remove_child(tree)
        tree = self.insert_tree(tree)
        if(old_parent.get_is_root_tree()):
            old_parent.mark = False
        elif(old_parent.mark):
            old_parent.mark = False
            return self.cascading_cut(old_parent)            
        else:
            old_parent.mark = True
        return tree
        
            
        

    def print_heap(self):
        print("Printing Heap")
        print("Root\tDepth1\tDepth2\tetc...")
        t = self.min_tree
        while True:
            if(t == self.min_tree):
                print("*" + str(t.value))
            else:
                print(str(t.value))
            t.print_children()
            t = t.right_sibling
            if(t == self.min_tree):
                break
        
        print("(* = Min Tree)")

    def delete(self, tree):
        self.decrease_key(tree, math.inf)
        self.extract_min()
        

class Tree:
    value = None;
    left_sibling = None;
    right_sibling = None;
    degree = None;
    children = None;
    parent = None
    mark = None
    
    def __init__(self, value, left_sibling= None, right_sibling = None):
        self.value = value;
        self.degree = 0
        self.children = list()
        self.parent = self
        self.mark = False
        if( not(left_sibling == None)):
            self.left_sibling = left_sibling;
        else:
             self.left_sibling = self;
        if( not(right_sibling == None)):
            self.right_sibling = right_sibling;
        else:
             self.right_sibling = self;
        

    def add_child(self, tree):
        tree.left_sibling = None
        tree.right_sibling = None
        tree.parent = self
        self.children.append(tree)       
        if(tree.degree > self.degree):
            self.degree = tree.degree + 1
        elif(tree.degree == self.degree):
            self.degree+=1

    def remove_child(self, tree):
        
        self.children.remove(tree)
        self.print_children()
        if(tree.degree+1 == self.degree):
            self.degree = -math.inf
            for child in self.children:
                if(child.degree > self.degree):
                    self.degree = child.degree
        return tree.value

    def print_children(self, tabindex = "\t"):
        if(len(self.children) == 0):
            return        
        else:
            for c in self.children:                
                print(tabindex + str(c.value))
                c.print_children(tabindex+"\t")

    def find_tree(self, value):
        if(len(self.children) == 0):
            return None
        for c in self.children:
            if(c.value == value):
                return c
            else:
                t = c.find_tree(value)
                if(not(t==None)):
                    return t
        return None

    def get_is_root_tree(self):
        return self.parent == self
        

            
        




f_heap=FibonacciHeap()
f_heap_values = list()
while len(f_heap_values) < 10:
    v = random.randint(-20, 20)    
    f_heap.insert(v)
    f_heap_values.append(v)

f_heap2 = FibonacciHeap()
while len(f_heap_values) < 20:
    v = random.randint(-20, 20)    
    f_heap2.insert(v)
    f_heap_values.append(v)
    
f_heap.union(f_heap2)

f_heap.print_heap()
m = f_heap.extract_min()
f_heap_values.remove(m)
print("\nGot Min: " + str(m) + "\n")

f_heap.print_heap()
m = f_heap.extract_min()
f_heap_values.remove(m)
print("\nGot Min: " + str(m) + "\n")
f_heap.print_heap()

f_heap_values.sort()

f_heap.print_heap()
t = f_heap.find_tree(f_heap_values.pop(5))

for i in range(11):
    print("\nDecreasing: " + str(t.value) + "\n")
    t = f_heap.decrease_key(t, 1)
f_heap_values.append(t.value)

f_heap.print_heap()
f_heap_values.sort()

t = f_heap.find_tree(f_heap_values.pop(5))
print("\nRemoving: " + str(t.value) + "\n")
f_heap.delete(t)

t = f_heap.find_tree(f_heap_values.pop(5))
print("\nRemoving: " + str(t.value) + "\n")
f_heap.delete(t)

f_heap.print_heap()

