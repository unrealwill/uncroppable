import cv2
import numpy as np

original = cv2.imread( "original.jpg")
#We drop the two Least Significant Bits
truncOriginal = 4*(original // 4)

uncroppable = truncOriginal.copy()

#We can store exactly 1 pixel every 4 pixels in the room we made for ourselves with the LSB 
#so we can store an half resolution image exactly
smalldim = (int(original.shape[1]/2),int(original.shape[0]/2))
smaller = cv2.resize(original,smalldim,interpolation=cv2.INTER_LANCZOS4)

#We show the loss of quality we can expect from the downscale/upscale procedure
originaldim = (int(original.shape[1]),int(original.shape[0]))
upscaled = cv2.resize(smaller, originaldim,interpolation=cv2.INTER_LANCZOS4 )

#We flatten the arrays to mix pixels and channels 
#(mixing channels is optional, not mixing them will result in 3 times less defective pixels but they will be more defective but easier for an ML algorithm to recover from)
channels = 1
#use channels = 1 to mix channels and channels = 3 to not mix channels
flatuncroppable = uncroppable.reshape(-1,channels)
flatsmaller = smaller.reshape(-1,channels)

#We will distribute the pixels randomly among the image to make it robust against any specific crop
#You will need to know the seed to be able to recover
#It's kind of a very weak secret key
np.random.seed(42)
perm = np.random.permutation(flatsmaller.shape[0])

#We distribute the 2 bits to the appropriate pixel
for k in range(4):
	bws = (cv2.bitwise_and( flatsmaller, 3*pow(4,k)) // (pow(4,k))).reshape(-1,channels)
	ind = k+4*perm
	flatuncroppable[ind]+=bws

#We now have an uncroppable image that will resist being cropped
uncroppable = flatuncroppable.reshape(original.shape)

#Let's crop Emily's face
cropped = uncroppable.copy()
cropped[40:120,150:250] = 0

#Let's recover from the crop
flatcropped = cropped.reshape(-1,channels)
lowbits = flatcropped % 4
flatrecover = np.zeros_like(smaller).reshape(-1,channels)
#We recompose the small resolution bytes from the bits by grabbing them at the right place
for k in range(4):
	ind = k + 4*perm
	flatrecover += lowbits[ind]*pow(4,k)

smallrecovered = flatrecover.reshape(smaller.shape)
recovered = cv2.resize(smallrecovered, originaldim,interpolation=cv2.INTER_LANCZOS4 )

cv2.imshow("original",original)
cv2.imshow("truncOriginal",truncOriginal)
cv2.imshow("smaller",smaller)
cv2.imshow("upscaled",upscaled)
cv2.imshow("uncroppable",uncroppable)

cv2.imshow("cropped",cropped)
cv2.imshow("smallrecovered",smallrecovered)
cv2.imshow("recovered",recovered)

cv2.imwrite("truncOriginal.png",truncOriginal)
cv2.imwrite("smaller.png",smaller)
cv2.imwrite("upscaled.png",upscaled)
cv2.imwrite("uncroppable.png",uncroppable)
cv2.imwrite("cropped.png",cropped)
cv2.imwrite("smallrecovered.png",smallrecovered)
cv2.imwrite("recovered.png",recovered)

cv2.waitKey(0)
