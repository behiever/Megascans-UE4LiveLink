# Megascans UE4 Integration - LiveLink

![Screenshot](/resources/HighresScreenshot00001.jpg)

The [Megascans LiveLink](https://www.megascans.se) for UE4 is a runtime plugin for Unreal Engine 4 that lets you import assets from the Megascans Library with just a few clicks. The plugin works with Megascans Bridge to give you the best library manager/importer/downloader tool for your assets.



The LiveLink is written 100% in Python using the [**UnrealEnginePython**](https://github.com/20tab/UnrealEnginePython) plugin for Unreal Engine 4, which is developed by :

Roberto De Ioris (20Tab S.r.l. http://20tab.com) with sponsorship from Accademia Italiana Videogiochi (http://aiv01.it), Kite & Lightning (http://kiteandlightning.la/) and GOODTH.INC (https://www.goodthinc.com/).


### Installing the Megascans LiveLink

![Screenshot](/resources/HighresScreenshot00000.jpg)

This plugin can be automatically installed with the help of Megascans Bridge, but if you want to do things manually
you should start by creating a folder "UnrealEnginePython" under this path : 
**C:\Program Files\Epic Games\UE_4.XX\Engine\Plugins\**.

Then put this project's content inside that folder. When installed through the Bridge the ms_Init.py file sets it's a custom
path for the custom_path variable, otherwise it autodetects that path, which basically corresponds to where the file itself is.  
Beside using a default Python 3.6 installation, the LiveLink comes with two other modules: Clipboard and PySide2. PySide2 is our main user interface library.  


The different Python files in the UnrealEnginePython folder are all called at one point or another by the LiveLink.

**ue_site.py** is executed on engine startup. It contains very basic code, mostly a call to another Python file.

**ms_Init.py** is used to initialize all our libraries and custom path.

**ms_setup.py** is where we create our toolbar button and initialize the livelink. This file is called in ue_site.py.

**ms_user_interface.py** contains all our UI-related code. Due to its creation being very recent/unexpected this file is expected to receive more updates on it’s documentation as we improve it’s core architecture into easily usable UI classes for custom pipeline user interfaces.

**ms_main.py** is where all our useful functions are stored. This is where we import the assets, create materials, import the main master materials, foliage assets, default noise masks, etc.

You’re probably going to be using ms_main.py most of the time, and to help you in that task, each function in this file has its own documentation tab with an example of how to call it.



### Writing your own asset importer

![Screenshot](/resources/HighresScreenshot00002.jpg)


The LiveLink gives you access to a set of useful commands, like this one to import a mesh for instance :

```python
ms_import_mesh('C:/Meshes/MyMesh.fbx', '/Game/Mesh_Folder')
```
Or this one to apply a texture map to a material instance :

```python
ms_apply_tex2d_to_inst(inst_uobject, '/Game/Textures/bark_Albedo', 'Albedo')
```


You could push this a lot further and write a relatively small file that automatically imports and sets up your assets : 



```python
# We start off by initializing the unreal_engine module, then we execute the Megascans LiveLink's ms_main.
import unreal_engine as ue
ue.exec('ms_main.py')
 
folderpath_ = "/Game/Wood_Tree"
 
# QFileDialog is a PySide2.QtGui class. We use it to open a file browser for the texture maps and another one for the mesh files.
Textures_Path = QFileDialog.getOpenFileNames(None, str("Select your texture maps"), "", str("Image Files (*.png *.jpg)"))
Mesh_Path = QFileDialog.getOpenFileNames(None, str("Select your geometry files"), "", str("Image Files (*.fbx *.obj)"))

texture_paths = Textures_Path[0]
meshes_ = Mesh_Path[0]

# ms_import_mesh is a ms_main function that imports a given mesh to the input path folderpath_.
for mesh_ in meshes_:
    ms_import_mesh(mesh_, folderpath_)


# ms_import_texture_list imports an array of textures to the input path folderpath_.
ms_import_texture_list(texture_paths, folderpath_)

# Now we create our material instance, which is based on the material Basic_Master.
parent_mat = ue.load_object(Material, "/Game/Basic_Master")
ms_create_material_instance(parent_mat, "Wood_Tree_inst", folderpath_)

# Then we load it.
inst_uobj = ue.load_object(MaterialInstance, folderpath_ + "/" + "Wood_Tree_inst")

# This will return a list of all the meshes available in the folderpath_ folder.
static_mesh_array = [[item, (folderpath_ + "/" + item.get_name())] for item in ue.get_assets(folderpath_) if item.is_a(StaticMesh)]

# Assigning a material instance to our geometry is done by calling ms_main's ms_inst_2_mesh function.
if mesh_path != None:
    ms_inst_2_mesh(inst_uobj, static_mesh_array)

# Once you have our material instance applied to the geometry, we can start applying the textures from texture_paths to the material instance.
for texture in [item for item in ue.get_assets(folderpath_) if item.is_a(Texture2D)]:
    try:
        text_input = ms_get_map(texture.get_name())
        text_input = "metallic" if text_input.lower() == "metalness" else text_input
 
        # This ms_main function takes the material instance's UObject, the texture's name and an str of the map type (albedo, normal, etc...).
        ms_apply_tex2d_to_inst(inst_uobj, texture.get_path_name(), text_input)
    except:
        pass
 
# Finally we sync the content browser to the folderpath_'s content.
ue.sync_browser_to_assets(ue.get_assets(folderpath_))

```



That file should give you an idea on how to interact with the Megascans LiveLink and UnrealEnginePython in general. If you have any questions feel free to check the UnrealEnginePython GitHub page or send a, email to adnan at quixel.se!

The Megascans LiveLink is hosted on GitHub under a GNU General Public License v3.0.
