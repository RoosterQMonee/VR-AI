import pygame as py;import os;import math as ma
def mm(a,b):
    ca,ra,cb,rb=len(a[0]),len(a),len(b[0]),len(b);rm=[[j for j in range(cb)]for i in range(ra)]
    if ca==rb:
        for x in range(ra):
            for y in range(cb):
                sum=0
                for k in range(ca):sum+=a[x][k]*b[k][y]
                rm[x][y]=sum
        return rm
    else:return None
os.environ["SDL_VIDEO_CENTERED"]='1';bl,wh,b,wi,h=(20,20,20),(230,230,230),(0,154,255),960,540;py.init();py.display.set_caption("3D Projection");w=py.display.set_mode((wi,h));clock=py.time.Clock();f,a,cp,sc,s=60,0,[wi//2,h//2],500,0.002;po=[n for n in range(8)];po[0]=[[-1],[-1],[1]];po[1]=[[1],[-1],[1]];po[2]=[[1],[1],[1]];po[3]=[[-1],[1],[1]];po[4]=[[-1],[-1],[-1]];po[5]=[[1],[-1],[-1]];po[6]=[[1],[1],[-1]];po[7]=[[-1],[1],[-1]]
def cpo(i,j,k):a,b=k[i],k[j];py.draw.line(w,bl,(a[0],a[1]),(b[0],b[1]),2)
while True:
    clock.tick(f);w.fill(wh);v=0;pp=[j for j in range(len(po))];rx=[[1,0,0],[0,ma.cos(a),-ma.sin(a)],[0,ma.sin(a),ma.cos(a)]];ry=[[ma.cos(a),0,-ma.sin(a)],[0,1,0],[ma.sin(a),0,ma.cos(a)]];rz=[[ma.cos(a),-ma.sin(a),0],[ma.sin(a),ma.cos(a),0],[0,0,1]]
    for p in po:rd=mm(ry, p);rd=mm(rx, rd);rd=mm(rz, rd);d=5;z=1/(d-rd[2][0]);pm=[[z,0,0],[0,z,0]];pd=mm(pm, rd);x,y=int(pd[0][0]*sc)+cp[0],int(pd[1][0]*sc)+cp[1];pp[v]=[x,y];py.draw.circle(w,b,(x,y),10);v+=1
    for m in range(4):cpo(m,(m+1)%4,pp),cpo(m+4,(m+1)%4+4,pp),cpo(m,m+4,pp);a+=s;py.display.update()