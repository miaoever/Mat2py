def int2str(self,curNode):
    self._CodeGen__emitCode("str(")
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__emitCode(")")
