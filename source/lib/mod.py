def mod(self,curNode):
    self._CodeGen__emitCode("((")
    self._CodeGen__genExp(curNode.child[0])
    self._CodeGen__emitCode(") % (")
    self._CodeGen__genExp(curNode.child[0].sibling)
    self._CodeGen__emitCode("))")
