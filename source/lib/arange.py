def arange(self,curNode):
    self._CodeGen__emitCode("np.arange(")
    curNode.child[0].attr = self._CodeGen__strDec(curNode.child[0])
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__emitCode(",")
    if len(curNode.child) == 3:
        self._CodeGen__genExp(curNode.child[2])
        self._CodeGen__emitCode(",")
        self._CodeGen__genExp(curNode.child[1])
    else:
        self._CodeGen__genExp(curNode.child[1])
    self._CodeGen__emitCode(")")
