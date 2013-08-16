def size(self,curNode):
    mat = curNode.child[0]
    self._CodeGen__genExp(mat)
    self._CodeGen__emitCode(".shape")
    if mat.sibling:
        self._CodeGen__emitCode("[")
        self._CodeGen__genExp(mat.sibling)
        self._CodeGen__emitCode("-1]")
