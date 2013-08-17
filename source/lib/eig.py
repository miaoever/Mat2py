def eig(self,curNode):
    self._CodeGen__emitCode("np.linalg.eig(")
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__visitSibling(curNode.child[0],self._CodeGen__genExp,", ")
    self._CodeGen__emitCode(")")
