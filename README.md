# Uncroppable
Make your image uncroppable

## The starting image :

![Original Image](original.jpg?raw=true "Original")

## The result : an almost identical image that can't be cropped

![Uncroppable Image](uncroppable.png?raw=true "Uncroppable")

Let's crop it anyway :

![Cropped Image](cropped.png?raw=true "cropped.png")

## Let's recover from it : 

If we mixed the channels : 

![Recovered mixed Channel Image](recoveredMixedChannels.png?raw=true "recoveredMixedChannels.png")

If we didn't mix the channels : 

![Recovered Unmixed Channel Image](recoveredUnmixedChannels.png?raw=true "recoveredUnmixedChannels.png")

## How it's done : 

We steganographically encode a permuted half resolution image in the two least significant bits of each pixel.

For more see the commented uncroppable.py file

Of course, this is just a proof of concept that is easily detectable with the appropriate software, and any advanced uncroppable image algorithm would use error correcting code and the compression codecs directly in the hardware encoder of your sensor, to make it harder to detect.
