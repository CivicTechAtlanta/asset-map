try:
  import xml.etree.ElementTree as ET  # python 2.5
except ImportError, e:
  import elementtree.ElementTree as ET  # older pythons
import KMLwriter