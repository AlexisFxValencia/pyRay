import sys
import pygame
import math

class RayCaster:
    def __init__(self):
        pygame.init()
        width, height = 800, 600
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Draggable Disks")

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.light_blue = (70, 70, 230)
        self.dark_blue = (20, 20, 100)
        self.white = (255, 255, 255)

        self.radius_cam = 5
        self.radius_obj= 50
        self.radius_light = 5

        self.camera_pos = pygame.math.Vector2(100, 200) 
        
        self.target_1_pos = pygame.math.Vector2(200, 200) 
        self.object_pos = pygame.math.Vector2(300, 200)
        self.light_pos = pygame.math.Vector2(500, 200) 
        
        

        self.dragging = None  # Variable to store the disk being dragged
        self.tolerance = 10
        
        self.intersect_pos = pygame.math.Vector2(0, 0) 
        self.screen_direction = pygame.math.Vector2(0, 0) 
        self.set_screen_direction()
        
        #options
        self.draw_lines = False
        self.object_visible = False

    def update_draging(self, event):
        if pygame.Rect(self.camera_pos.x - self.radius_cam, self.camera_pos.y - self.radius_cam, 2 * self.radius_cam, 2 * self.radius_cam).collidepoint(
                                event.pos):
            self.dragging = 'disk1'
        elif pygame.Rect(self.object_pos.x - self.radius_obj, self.object_pos.y - self.radius_obj, 2 * self.radius_obj, 2 * self.radius_obj).collidepoint(
                event.pos):
            self.dragging = 'disk2'
        elif pygame.Rect(self.light_pos.x - self.radius_light, self.light_pos.y - self.radius_light, 2 * self.radius_light, 2 * self.radius_light).collidepoint(
                event.pos):
            self.dragging = 'disk3'
        elif pygame.Rect(self.target_1_pos.x - self.radius_light, self.target_1_pos.y - self.radius_light, 2 * self.radius_light, 2 * self.radius_light).collidepoint(
                event.pos):
            self.dragging = 'target_1'


    def update_disk_position(self, event_pos):
        if self.dragging == 'disk1':
            self.camera_pos.x = event_pos[0]
            self.camera_pos.y = event_pos[1]
        elif self.dragging == 'disk2':
            self.object_pos.x = event_pos[0]
            self.object_pos.y = event_pos[1]
        elif self.dragging == 'disk3':
            self.light_pos.x = event_pos[0]
            self.light_pos.y = event_pos[1]
        elif self.dragging == 'target_1':
            self.target_1_pos.x = event_pos[0]
            self.target_1_pos.y = event_pos[1]
            self.set_screen_direction()

    def intersect_disk(self, origin, direction, disk_center, radius):
        delta = disk_center - origin
        m_beta = 2*(direction.x*delta.x + direction.y*delta.y)
        gamma = delta.length_squared() - radius**2
        discr = m_beta**2 - 4 * gamma        
        if discr == 0:
            s = m_beta/2
            point = origin + s * direction
            return [point]
        elif discr > 0:
            root_discr = math.sqrt(discr)
            s1 = 0.5*(m_beta - root_discr)
            s2 = 0.5*(m_beta + root_discr)
            points = []
            if s1 > self.tolerance:
                point1 = origin + s1 * direction
                points.append(point1)
            if s2 > self.tolerance:
                point2 = origin + s2 * direction
                points.append(point2)           
            return points
        else:
            return []


    def compute_unit_vector(self, pos_depart, pos_arrival):
        v = pos_arrival - pos_depart
        norm = v[0]**2 + v[1]**2
        norm = math.sqrt(norm)
        v = v/norm
        return v
     
    
 
    def plot_one_lighted_point(self, target_pos):
        primary_vec = self.compute_unit_vector(self.camera_pos, target_pos)            
        intersections = self.intersect_disk(self.camera_pos, primary_vec, self.object_pos, self.radius_obj)
        
        if len(intersections) != 0 :   
            self.intersect_pos = intersections[0] 
            if self.draw_lines:
                pygame.draw.line(self.screen, self.white, self.camera_pos, self.intersect_pos, 2)
                pygame.draw.line(self.screen, self.white, self.intersect_pos, self.light_pos, 2)

        
            shading_vec = self.compute_unit_vector(self.intersect_pos, self.light_pos)
            intersections_shading = self.intersect_disk(self.intersect_pos, shading_vec, self.object_pos, self.radius_obj)
            if len(intersections_shading) == 0:
                pygame.draw.circle(self.screen, self.light_blue, self.intersect_pos, self.radius_light)
            elif len(intersections_shading) == 1:
                pygame.draw.circle(self.screen, self.dark_blue, self.intersect_pos, self.radius_light)


    def set_screen_direction(self):
                self.screen_direction = self.compute_unit_vector(self.camera_pos, self.target_1_pos)
                self.screen_direction = self.screen_direction.rotate(90)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            self.update_draging(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.dragging = None
                    elif event.type == pygame.MOUSEMOTION:
                        self.update_disk_position(event.pos)

            # Draw disks
            self.screen.fill(self.black)
            pygame.draw.circle(self.screen, self.red, self.camera_pos, self.radius_cam)
            pygame.draw.circle(self.screen, self.blue, self.light_pos, self.radius_light)
            if self.object_visible:
                pygame.draw.circle(self.screen, self.green, self.object_pos, self.radius_obj)
            pygame.draw.circle(self.screen, self.white, self.target_1_pos, self.radius_light)

            
            #self.plot_one_lighted_point(self.target_1_pos)
            
            
            screen_size = 40
            i_begin = -20
            i_end = 20
            begin_pos = self.target_1_pos + self.screen_direction * i_begin
            end_pos = self.target_1_pos + self.screen_direction * i_end
            pygame.draw.line(self.screen, self.red, begin_pos, end_pos)
            
            for i in range(i_begin, i_end):            
                target_2_pos = self.target_1_pos + self.screen_direction * i
                self.plot_one_lighted_point(target_2_pos)
            
                        
            pygame.display.flip()

if __name__=="__main__":
    print("toto")
    rc = RayCaster()
    rc.run()