class AVLTreeNode(object):
    def __init__(self, key, value, parent):
        """[key]: comparable object, usually """
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent
        self.count = 1
        self.height = 0

    def __repr__(self):
        if self.left is None and self.right is None: return "<{}→{},({})>".format(self.key, self.value, self.balance())
        elif self.left is None: return "<{}→{},({})|{}>[{}]".format(self.key, self.value, self.balance(),
                                                   self.right_count(), self.right)
        elif self.right is None:return "[{}]<{}|{}→{},({})>".format(self.left,self.left_count(),self.key,self.value,self.balance())
        return "[{}]<{}|{}→{},({})|{}>[{}]".format(self.left,self.left_count(),self.key,self.value,self.balance(),self.right_count(),self.right)

    def left_count(self):
        return self.left.count if self.left else 0

    def right_count(self):
        return self.right.count if self.right else 0

    def balance(self):
        return (self.right.height if self.right else 0) - (self.left.height if self.left else 0)

    def _update_count(self):
        self.count = (self.left.count if self.left else 0)+(self.right.count if self.right else 0)+1

    def _update_height(self):
        self.height = max((self.left.height if self.left else 0),(self.right.height if self.right else 0))+1

    def _left_rot(self):
        assert(self is not None and self.right is not None),self
        print("left rot {},right {} :{}".format(self.key, self.right.key, self))
        right = self.right
        parent = self.parent
        inner = self.right.left

        self.parent = right
        self.right = inner
        if inner: inner.parent=self
        right.parent = parent
        right.left = self
        if parent:
            if parent.left is self: parent.left = right
            else:
                assert(parent.right is self)
                parent.right = right

        #print("right parent {}, left {}, right {}".format(right.parent,right.left,right.right))
        self._update_count()
        self._update_height()
        right._update_count()
        right._update_height()
        #print("get {}".format(right))
        return right

    def _right_rot(self): # symmetric
        print("right rot {}".format(self))
        assert(self is not None and self.left is not None)
        left = self.left
        parent = self.parent
        inner = self.left.right

        self.parent = left
        self.left = inner
        if inner: inner.parent=self
        left.parent = parent
        left.right = self
        if parent:
            if parent.right is self: parent.right = left
            else: parent.left = left

        self._update_count()
        self._update_height()
        left._update_count()
        left._update_height()
        #print("get {}".format(left))
        return left

    def _left_right_rot(self):
        print("<left right rot>")
        assert(self is not None and self.left is not None)
        self.left._left_rot()
        return self._right_rot()

    def _right_left_rot(self):
        print("<right left rot>")
        assert (self is not None and self.right is not None)
        self.right._right_rot()
        return self._left_rot()

    def __len__(self):
        return self.count


class AVLTree(object):
    def __init__(self):
        self.root = None
        self.keys = set()

    def __repr__(self):
        return str(self.root)

    def _insert(self, key, value, node, parent):
        if node is None:
            node = AVLTreeNode(key, value, parent)
        elif key < node.key:
            node.left = self._insert(key,value, node.left, node)
            node.count +=1
            if node.balance() == -2:
                if key < node.left.key:
                    node = node._right_rot()
                else:
                    node = node._left_right_rot()
        elif key > node.key:
            node.right = self._insert(key, value, node.right, node)
            node.count +=1
            if node.balance() == 2:
                if key > node.right.key:
                    node = node._left_rot()
                else:
                    node = node._right_left_rot()
        else:
            assert(False),"Duplicate Key"

        node._update_height()
        return node

    def insert(self, key, value):
        """Insert certain value into the tree, worst case O(log n)"""
        self.root = self._insert(key,value, self.root, None)

    def get_len(self):
        """get the length of the tree, worst case O(1)"""
        return len(self.root) if self.root is not None else 0


    def exist(self, key):
        """ Return if one key exist in the tree. worst case O(1)"""
        return key in self.keys

    def _get_node(self, key):
        """ Return node corresponding to key or None, worst case O(log n) """
        if not self.exist(key): return None
        it = self.root
        while True:
            if it.key > key:
                it=it.left
                continue
            elif it.key < key:
                it=it.right
                continue
            else:
                return it

    def get(self,key):
        """Return value corresponding to key, worst case O(log n)"""
        node = self._get_node(key)
        assert(node is not None)
        return node.value

    def set(self, key, value):
        """Set corrresponding value to a key, worst case O(log n)"""
        node = self._get_node(key)
        assert (node is not None), "cannot find key to set"
        node.value = value

    def get_index(self, key):
        """ Return the index of certain key, worst case O(log n)"""
        node = self._get_node(key)
        assert(node is not None),"Invalid key to be indexed"
        it = node
        total_count = node.left_count()
        while it.parent is not None:
            parent = it.parent
            if parent.right is it:
                total_count += parent.left_count() + 1
            it = parent
        return total_count

    def __getitem__(self, idx):
        """Get (key,value) via certain index, worst case O(log n)"""
        assert(type(idx) is int),"Not compatible value"
        assert(self.root and 0<=idx<self.root.count),"Out of range"
        it = self.root
        while it is not None:
            print(it.key,it.left_count(),idx)
            left_count = it.left_count()
            if idx < left_count:
                it = it.left
                continue
            elif idx > left_count:
                it = it.right
                idx -= left_count+1
                continue
            else:
                return it
        return None


    def _delete(self, node, delete_node):
        assert(False),"Not Implemented"
        if node is None or delete_node is None:
            return None
        elif delete_node.key < node.key:
            node.left = self._delete(node.left, delete_node)
            node.count -=1
            if node.balance() == 2:
                right = node.right
                if right.balance() < 0:
                    node = node._right_left_rot()
                else:
                    node = node._left_rot()
        elif delete_node.key > node.key:
            node.right = self._delet(node.right, delete_node)
            node.count -=1
            if node.balance() == -2:
                left = node.left
                if left.balance() > 0:
                    node = node._left_right_rot()
                else:
                    node = node._right_rot()
        else: # hit the node
            if tree.left and tree.right:

            else:



    def delete(self, key):
        node = self._get_node(key)
        assert(node is not None),"Invalid key to be deleted"
        self.keys.remove(key)



    def iterate(self):
        """Return (key, value) pair in asending order, O(n)"""
        # TODO: iterative implementation
        for pair in self._iterate(self.root):
            yield pair

    def _iterate(self, node):
        if node is None: return
        if node.left is not None:
            for pair in self._iterate(node.left):
                yield pair
        yield node.key,node.value
        if node.right is not None:
            for pair in self._iterate(node.right):
                yield pair



if __name__=="__main__":
    tree=AVLTree()
    for i in [3,2,1,4,5,6,7,16,15,14,13,12,11,10,8,9]:
        print("insert {}".format(i))
        tree.insert(i,i)
        print(tree)
        print(list(tree.iterate()))
        print(tree[tree.get_index(i)])