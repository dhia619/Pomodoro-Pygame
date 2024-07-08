import pygame

pygame.init()

class Entry:
	def __init__(self,x,y,w,h,font):
		self.rect = pygame.Rect(x,y,w,h)
		self.on_focus = False
		self.on_B_color = (240,137,143)
		self.off_B_color = (20,200,109)
		self.border_color = self.off_B_color
		self.text = ""
		self.text_surface = font.render(self.text,True,(0,0,0))

	def draw(self,surface):
		pygame.draw.rect(surface,self.border_color,self.rect,2,border_radius = 10)
		surface.blit(self.text_surface,(self.rect.x+5,self.rect.y+6//2))
	def update(self):
		if self.on_focus:
			self.border_color = self.on_B_color
		else:
			self.border_color = self.off_B_color