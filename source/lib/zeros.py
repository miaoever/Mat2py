def zeros(self,curNode):
    self._CodeGen__emitCode("np.zeros(")
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__emitCode(")")
