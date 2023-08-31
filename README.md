# German Public Building Section Dataset (GPUB)

GPUB includes aerial data publicly provided by the opengeodata initiative of the government of the federal state of North-Rhine-Westphalia, Germany.

GPUB is created because there is a lack of public building instance segmentation datasets that also contain digital surface model (DSM) information. GPUB contributes to the developement of multi-modal building detection methods by deep learning methods.

## GPUB: Section Dataset
Link to the dataset: https://zenodo.org/record/8304900

## Roof3D: Section+Plane Dataset (Public + Manual + Synthetic)
Link to the dataset: https://zenodo.org/record/8300629

With the following code, you can decode the run-length-encoded segmentations to masks:

```python
from pycocotools.mask import frPyObjects, decode
import json

with open("path_to_annotation.json",'r') as f:
  annotations = json.load(f)

annos = annotations["annotations"]

rle = annos[201]["segmentation"]

rle = frPyObjects(rle, rle.get(‘size’)[0], rle.get(‘size’)[1])
mask = decode(rle)
```

With the script 'visRoof3D.py', the patches can be visualized sequentially.

### Locations of the real part of the dataset
![alt text](https://github.com/dlrPHS/GPUB/blob/main/maploc.jpg?raw=true)

#### Distribution in Cologne, Germany
Red color indicates training area, green color indicates test area.
![alt text](https://github.com/dlrPHS/GPUB/blob/main/köln_maploc.jpg?raw=true)

#### Distribution in Berlin, Germany
Red color indicates training area.
![alt text](https://github.com/dlrPHS/GPUB/blob/main/berlin_maploc.jpg?raw=true)
