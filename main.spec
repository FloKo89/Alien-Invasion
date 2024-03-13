# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['E:/Github/My-SpaceInvaders'],
             binaries=[],
             datas=[
                ('E:/Github/My-SpaceInvaders/assets/Help_Screen', 'assets/Help_Screen'),
                 ('E:/Github/My-SpaceInvaders/assets/Boss1', 'assets/Boss1'),
                 ('E:/Github/My-SpaceInvaders/assets/Enemies', 'assets/Enemies'),
                 ('E:/Github/My-SpaceInvaders/assets/Explosions', 'assets/Explosions'),
                 ('E:/Github/My-SpaceInvaders/assets/Player', 'assets/Player'),
                 ('E:/Github/My-SpaceInvaders/movie', 'movie'),
                 ('E:/Github/My-SpaceInvaders/sound', 'sound'),
                 ('E:/Github/My-SpaceInvaders/languages', 'languages'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Alien Invasion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='icon.ico') 
