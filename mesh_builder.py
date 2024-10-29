from config import *

def build_triangle_mesh() -> tuple[int, int]:
    vertex_data = np.zeros(3, dtype = data_type_vertex)
    vertex_data[0] = (-1.0, -1.0, 0.0, 0)
    vertex_data[1] = (1.0, -1.0, 0.0, 1)
    vertex_data[2] = (1.0, 1.0, 0.0, 2)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    attrib_index = 0
    size = 3
    stride = data_type_vertex.itemsize
    offset = 0
    glVertexAttribPointer(attrib_index, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attrib_index)

    offset += 12

    attrib_index = 1
    size = 1
    glVertexAttribIPointer(attrib_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attrib_index)
    
    return (vbo, vao)



def build_quad_mesh() -> tuple[int, int, int]:
    vertex_data = np.zeros(4, dtype = data_type_vertex)
    vertex_data[0] = (-1,-1, 0.0, 0)
    vertex_data[1] = ( 1,-1, 0.0, 1)
    vertex_data[2] = ( 1, 1, 0.0, 2)
    vertex_data[3] = (-1, 1, 0.0, 1)

    index_data = np.array((0,1,2,2,3,0), dtype=np.ubyte)


    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    attrib_index = 0
    size = 3
    stride = data_type_vertex.itemsize
    offset = 0
    glVertexAttribPointer(attrib_index, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attrib_index)

    offset += 12

    attrib_index = 1
    size = 1
    glVertexAttribIPointer(attrib_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attrib_index)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

    
    return (ebo, vbo, vao)
