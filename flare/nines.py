import pygame

def image_at(sheet, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.SRCALPHA)
        image.blit(sheet, (0, 0), rect)
        
        return image

def nines(s:pygame.Surface,rect:pygame.Rect):
    TL = image_at(s,(00,00,16,16))
    TC = image_at(s,(16,00,16,16))
    TR = image_at(s,(32,00,16,16))
    
    CL = image_at(s,(00,16,16,16))
    CC = image_at(s,(16,16,16,16))
    CR = image_at(s,(32,16,16,16))
    
    BL = image_at(s,(00,32,16,16))
    BC = image_at(s,(16,32,16,16))
    BR = image_at(s,(32,32,16,16))
    
    TCF = pygame.transform.scale(TC,(rect.w-32,16))
    BCF = pygame.transform.scale(BC,(rect.w-32,16))
    
    CLF = pygame.transform.scale(CL,(16,rect.h-32))
    CRF = pygame.transform.scale(CR,(16,rect.h-32))
    
    CCF = pygame.transform.scale(CC,(rect.w-32,rect.h-32))
    
    ns = pygame.Surface(rect.size,pygame.SRCALPHA)
    ns.blit(TL,(0,0))
    ns.blit(TCF,(16,0))
    ns.blit(TR,(rect.width-16,0))
    
    ns.blit(CLF,(0,16))
    ns.blit(CRF,(rect.width-16,16))
    
    ns.blit(CCF,(16,16))
    
    
    ns.blit(BL,(0,rect.h-16))
    ns.blit(BCF,(16,rect.h-16))
    ns.blit(BR,(rect.width-16,rect.h-16))
    
    return ns