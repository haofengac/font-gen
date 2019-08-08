
from gftools.fonts_public_pb2 import FamilyProto
from google.protobuf import text_format
from IPython.display import SVG

def show_svg(path):
    return SVG(url=path)

def read_metadata(fp):
    # check category
    with open(fp) as f:
        metadata = FamilyProto()
        text_data = f.read()

    text_format.Merge(text_data, metadata)
    return metadata
