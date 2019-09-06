# -*- mode: python -*-

block_cipher = None


a = Analysis(['sanicapp.py', 'adbinstall.py'],
             pathex=['/Users/dinesh.duraisamy/Documents/js_learnings/electron/adb_sanic'],
             binaries=[],
             datas=[( '/Users/dinesh.duraisamy/Documents/js_learnings/electron/adb_sanic/static', './static')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='sanicapp',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='sanicapp')
