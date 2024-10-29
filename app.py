from config import *
import mesh_builder

'''
class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Eye:

    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        self.theta = 0
        self.phi = 0
        self.update_vectors()

    def update_vectors(self):

        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )
        globalUp = np.array([0,0,1], dtype=np.float32)
        self.right = np.cross(self.forwards, globalUp) 
        self.up = np.cross(self.right, self.forwards)   

class Scene:

    def __init__(self):

        self.cubes = [
            Cube (
                position = [6,0,0],
                eulers = [0,0,0]
            )
        ]
        self.eye = Eye(position=[0,0,2])

    def update(self, rate):

        for cube in self.cubes:
            cube.eulers[1] += 0.25 * rate
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360

'''

class App:

    def __init__(self):

        self.eye_position = [np.float64(0.0),np.float64(0.0)]
        self.eye_zoom = np.float64(1.0)

        self.initialize_glfw()
        self.initialize_opengl()  
        self.run()
    
    def initialize_glfw(self) -> None:
        glfw.init()
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
            GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
        )

        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Render", None, None)
        glfw.make_context_current(self.window)

    def initialize_opengl(self) -> None:

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        #self.triangle_vbo, self.triangle_vao = mesh_builder.build_triangle_mesh()
        self.quad_ebo, self.quad_vbo, self.quad_vao = mesh_builder.build_quad_mesh()
        self.shader = create_shader_program("Mandelbrot_Shader/shaders/vertex.txt", "Mandelbrot_Shader/shaders/fragment.txt")
        self.u_time_location = glGetUniformLocation(self.shader, "u_time")
        
        
    def run(self):
        last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            pan_speed = 0.04 / self.eye_zoom
            zoom_speed = 1.033
            # Measure the time for each frame
            current_time = glfw.get_time()
            frame_duration = current_time - last_time
            last_time = current_time

            # Calculate FPS
            fps = 1.0 / frame_duration if frame_duration > 0 else 0
            glfw.set_window_title(self.window, f"Zoom: {self.eye_zoom:.2f} x  -  Center: ( {self.eye_position[0]:.3f} + {self.eye_position[1]:.3f} i )  -  Render - FPS: {fps:.2f}")

            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break
                
            # Capture pan and zoom inputs
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_UP) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_position[1] += pan_speed
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_DOWN) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_position[1] -= pan_speed
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_position[0] -= pan_speed
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_RIGHT) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_position[0] += pan_speed
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_B) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_zoom /= zoom_speed
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_F) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_zoom *= zoom_speed 
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_R) == GLFW_CONSTANTS.GLFW_PRESS:
                self.eye_zoom  = 1
                self.eye_position[0] = 0.0
                self.eye_position[1] = 0.0


            # Apply pan limits
            self.eye_position[0] = max(-2.0, min(2.0, self.eye_position[0]))
            self.eye_position[1] = max(-2.0, min(2.0, self.eye_position[1]))

            # Apply zoom limits
            self.eye_zoom = max(1.0, min(100000.0, self.eye_zoom))


            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.shader)

            #glBindVertexArray(self.triangle_vao)
            #glDrawArrays(GL_TRIANGLES, 0,3)
            glUniform1f(self.u_time_location, current_time)
            glUniform2d(glGetUniformLocation(self.shader,"center"), self.eye_position[0], self.eye_position[1])
            glUniform1f(glGetUniformLocation(self.shader, "zoom"), np.sqrt(self.eye_zoom))

            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)
            
            glfw.swap_buffers(self.window)


        self.quit()

    def quit(self):
        #glDeleteBuffers(1, (self.triangle_vbo,))
        glDeleteBuffers(2, (self.quad_ebo, self.quad_vbo))
        #glDeleteVertexArrays(1, (self.triangle_vao,))
        glDeleteVertexArrays(1, (self.quad_vao,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == "__main__":
    my_app = App()