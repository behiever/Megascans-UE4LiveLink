#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ███╗   ███╗███████╗ ██████╗  █████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗███████╗    ██╗███╗   ██╗████████╗███████╗ ██████╗ ██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ████╗ ████║██╔════╝██╔════╝ ██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║██╔════╝    ██║████╗  ██║╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██╔████╔██║█████╗  ██║  ███╗███████║███████╗██║     ███████║██╔██╗ ██║███████╗    ██║██╔██╗ ██║   ██║   █████╗  ██║  ███╗██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║╚════██║    ██║██║╚██╗██║   ██║   ██╔══╝  ██║   ██║██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║███████║╚██████╗██║  ██║██║ ╚████║███████║    ██║██║ ╚████║   ██║   ███████╗╚██████╔╝██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Quixel AB - Megascans Project
# The Megascans Integration for Unreal Engine 4 was written in Python, using the UnrealEnginePython plugin
# by 20Tab : https://github.com/20tab/UnrealEnginePython

# Megascans : https://megascans.se

# This integration gives you a LiveLink between Megascans Bridge and Unreal Engine 4. The source code is all exposed
# and documented for you to use it as you wish (within the Megascans EULA limits, that is).
# We provide a set of useful functions for importing data inside the engine, but you can use the default
# functions (of UnrealEnginePython) instead of Megascans modules if you want.

# We've tried to document the code as much as we could within a short timeframe, so if you're having any issues
# please send me an email (adnan@quixel.se) for support.


# ms_Init is the main function used to call the modules we might be in need of during the plugin's execution.
# This file is called on editor start and is a requirement as a first-line import command when working with the integration API.


import unreal_engine as ue
import json, re, os, sys, asyncio, traceback, ctypes, time, clipboard, webbrowser, inspect
from pprint import pprint

from unreal_engine.enums import EMaterialSamplerType, EHorizontalAlignment, EVerticalAlignment

from unreal_engine import SWindow, SVerticalBox, SHorizontalBox, SButton, STextBlock, SBorder, FLinearColor, FMaterialEditorUtilities, FSlateIcon, FSlateStyleSet

from pprint import pprint
from unreal_engine.structs import SlateBrush, SlateColor, Vector2D, SkeletalMaterial, MeshUVChannelInfo, ColorMaterialInput, VectorMaterialInput, ScalarMaterialInput, ExpressionInput

from unreal_engine.classes import MaterialInstanceConstant, MaterialInstance, StaticMeshActor, FoliageType
from unreal_engine.classes import StaticMesh, PyFbxFactory, MaterialExpressionTextureSample, MaterialFactoryNew, Material, TextureFactory, Texture2D


custom_path = None

# We're going to use this method post-launch to get the current installation path.

#path_ = (os.path.dirname(os.path.realpath('ms_Init')))
#path_ = os.path.split(os.path.split(path_)[0])[0]
#custom_path = os.path.join(path_, 'Plugins', 'UnrealEnginePython')


print('#'*20 + '-'*10 + 'Python Integration for Megascans Initialized' + '-'*10 + '#'*20)

if custom_path != None and not os.path.exists(os.path.join(custom_path, 'megascans')):
    custom_path = (r"CUSTOMPROJECTPATH" + "/")

def ms_return_path():
    return (custom_path)

print(custom_path)

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    ue.message_dialog_open(0, "C++ project detected, the integration UI is currently only available in a blueprint project.\n\
You can still use the plugin as normal, and expect C++ compatibility soon !")
    print('C++ Project Detected, UI not available in the current version.')
    pass

