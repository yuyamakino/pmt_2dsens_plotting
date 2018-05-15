#
# To show a scatter plot with polar coordinate as if it is histogram! 
#
from pylab import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

R_ZEN_STAGE=300.0; # 30 cm
MAX_STAGE_RANGE_FROM_ZEN_CENTER = 260.0; # distance along the stage from Zenith Center to the long-side edge  
MAX_ZEN_SCAN_ANGLE=math.asin( MAX_STAGE_RANGE_FROM_ZEN_CENTER/R_ZEN_STAGE ); # radian
MAX_ZEN_BIN = 64
MAX_AZI_BIN = 72

# Load the target file 
data = np.loadtxt('./sample_data.tab', skiprows=1) 

azi_angles = data[:,0]
zen_angles = data[:,1]
eff = data[:,2]
rms = data[:,3]

print eff.size

# Edges... 
phai = array([2*pi/(MAX_AZI_BIN) * n for n in range(MAX_AZI_BIN+1)]) 
th = array([ i*(MAX_ZEN_SCAN_ANGLE/(MAX_ZEN_BIN)) *(180./pi) for i in range(MAX_ZEN_BIN+1) ])
# Contents...
c = array([[ eff[x+MAX_ZEN_BIN*y] for y in range( phai.size-1 )] for x in range( th.size-1 ) ] )

plt.figure(figsize=(8, 8))
ax = subplot(111, projection='polar')

Phai = phai
# following alternative line is useful for the case where the number of azimuth bin is small
#Phai = cbook.simple_linear_interpolation(phai, 10)

#
# Note that sizes of 'C' and 'c' are different!! 
# Data taken at (azi_bin=0, zen_bin=i) are filled to the bins, (azi_angle=0-5, zen_angle>0).
#
C = zeros((th.size, Phai.size))
print 'C size', C.size
print 'c size', c.size

oldfill = 0
Phai_ = Phai.tolist()

for i in range( phai.size-1 ):
    fillto = Phai_.index(phai[i]) 
    fillto += 1 # to avoid 0:0 at the beggining... 
    #print oldfill, fillto 
    for j, x in enumerate(c[:,i]):    # keyword : 'extended_slicing'
        C[j, oldfill:fillto].fill(x)

    oldfill = fillto

# The plotting
phai, th = meshgrid(Phai, th)

#ax.pcolormesh(phai, th, C)
ax.pcolormesh(phai, th, C, vmin=.0, vmax=1.1)

ax.grid(True)
ax.set_rlim(0, 55)
ax.tick_params(labelsize=16)

PCM=ax.get_children()[2]
cbar = plt.colorbar(PCM, ax=ax, shrink=0.9, pad=0.1 ) # 4th argument to shift the z-axis

cbar.ax.tick_params(labelsize=16)
cbar.ax.set_ylabel('Relative sensitivity', size=18)
#savefig('cemap.pdf') # must be before show()
show()

