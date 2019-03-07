from setuptools import setup
  
setup(
    name="OverworkDeath",
    options = {
        'build_apps': {
            'include_patterns': [
		'**/*.ttf',
                '**/*.wav',
                '**/*.ogg',
		'**/*.cfg',
                '**/*_wire.egg',
		'**/*_model.egg',
            ],
            'gui_apps': {'OverworkDeath': 'main.py'},
            'platforms': [
                'manylinux1_x86_64',
                'macosx_10_6_x86_64',
                'win_amd64',
                'win32',
             ],
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
         }
     }
)
