# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:/Users/jsant/OneDrive/Images/Documents/projet-groupe-G/Cyclos/__main__.py'],
             pathex=['C:\\Users\\jsant\\OneDrive\\Images\\Documents\\projet-groupe-G\\Cyclos'],
             binaries=[],
             datas=[('C:/Users/jsant/OneDrive/Images/Documents/projet-groupe-G/Cyclos/data', '.'), ('D:\\ProgramData\\Anaconda3\\envs\\Cyclos37\\tcl\\tk*', 'tk/'), ('D:\\ProgramData\\Anaconda3\\envs\\Cyclos37\\tcl\\tcl*', 'tcl/')],
             hiddenimports=['pkg_resources.py2_warn', 'encodings'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['src.tests'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Cyclos',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\jsant\\OneDrive\\Images\\Documents\\projet-groupe-G\\Cyclos\\cyclos.ico')
