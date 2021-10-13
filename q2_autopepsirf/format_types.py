import os

import qiime2.plugin.model as model
from qiime2.plugin import SemanticType

# Define a new semantic type. This is really just an abstract symbol which
# can be used to constrain/define valid compositions of actions.
Slides = SemanticType('Slides')


class RevealSectionsFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        # TODO: ran out of time
        pass


class RevealAssetFormat(model.BinaryFileFormat):
    def _validate_(self, level='min'):
        # This is for any file that will be embeded in the presentation
        # there is no particular requirement for these files and they may
        # be anything.
        pass


class RevealSectionsDirFmt(model.DirectoryFormat):
    slides = model.File('slides.html', format=RevealSectionsFormat)
    assets = model.FileCollection('assets/.*', format=RevealAssetFormat)

    @assets.set_path_maker
    def assets_pathmaker(path):
        return os.path.join('assets', path)