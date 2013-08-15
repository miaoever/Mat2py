def max(self,curNode):
    self._CodeGen__emitCode("np.max(")
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__emitCode(")")
