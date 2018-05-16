#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# ███████╗████████╗ █████╗ ███╗   ██╗██████╗  █████╗ ██████╗ ██████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# ███████╗   ██║   ███████║██╔██╗ ██║██║  ██║███████║██████╔╝██║  ██║    █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ╚════██║   ██║   ██╔══██║██║╚██╗██║██║  ██║██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ███████║   ██║   ██║  ██║██║ ╚████║██████╔╝██║  ██║██║  ██║██████╔╝    ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                                                                                                                 

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Quixel AB - Megascans Project
# The Megascans Integration for Unreal Engine 4 was written in Python, using the UnrealEnginePython plugin
# by 20Tab : https://github.com/20tab/UnrealEnginePython

# This integration gives you a LiveLink between Megascans Bridge and Unreal Engine 4. The source code is all exposed
# and documented for you to use it as you wish (within the Megascans EULA limits, that is).
# We provide a set of useful functions for importing data inside the engine, but you can use the default
# functions (of UnrealEnginePython) instead of Megascans modules if you want.

# We've tried to document the code as much as we could within a short timeframe, so if you're having any issues
# please send me an email (adnan@quixel.se) for support.


# ms_main contains all the utility functions we're using in the livelink to import data, setup materials, create foliage, instances, etc...
# There are quite a few functions in here that aren't used anymore but can still be useful as we integrate more features into the livelink.*
# Most functions in here come with a quick explanation, the required input(s) and an example showing how it works.
# This will all be organized in a better way later on to allow you to browse the functions and their documentation in a more
# visually pleasing interface.



# This is the list of currently supported texture maps by the Megascans Integration
sup_maps = ['albedo', 'normal', 'displacement', 'opacity', 'translucency',
                    'gloss', 'specular', 'roughness', 'metalness', 'fuzz',
                    'bump', 'cavity', 'ao', 'mask', 'brush', 'metallic', 'diffuse']


# The following function takes a string and a material, then return the equivalent node to the input string
def ms_find_param(Label, Material_):
    output_ = None
    lister_ = Material_.Expressions
    object_ = ""
    for object_ in lister_:
        try:
            if object_.DESC.lower() == Label.lower():
                output_ = object_
                print("PARAMETER NAME  -  " + str(object_.DESC))
                break
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            pass
    return object_



# The following function checks if a given UObject exists
def ms_obj_exists(UObject_Path):

    Value = False
    get_obj = None
    try:
        get_obj = ue.find_object(UObject_Path)
        if get_obj != None:
            Value = True
    except:
        Value = False

    return Value

# The following function returns the type (albedo, normal, etc...) of a texture map from a given texture name.
def ms_get_map(map_name):

    if '.' in map_name:
        val_ = [item.lower() for item in map_name.split('.')[-2].split('_')]
    else:
        val_ = [item.lower() for item in map_name.split('_')]

    return [item.lower() for item in sup_maps if item.lower() in val_][0]

# The following function checks if a given UObject exists. This function should replace ms_obj_exists.
def ms_instance_exists(ex_path):
  inst_ = False
  try:
      inst_ = ue.load_object(MaterialInstance, ex_path)
  except:
      inst_ = False
      print("Couldn't create material, maybe it already exists ?\n")

  return inst_

# The following function takes a UObject material and a string request corresponding to a node's name, then returns it's UObject.
def ms_find_input_node(material, request_):
    _data_ = None
    try:
        for item in material.Expressions:
            if item.get_name().lower() == request_.lower():
                _data_ = item
                break
    except:
        pass
    return _data_


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_get_asset_type takes the json data from the Bridge export as an input, then returns the human-readable version of it's version ('3D Asset' for example).
# The function takes 1 arguments: 
#- A json file that corresponds to the Bridge's raw json output


# Usage example ():

#ms_get_asset_type(json_parse)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_get_asset_type(json_parse):

    try:
        with open(os.path.join(json_parse['path'], json_parse['id'] + '.json')) as f:
                        json_check = f.read()

        json_check = json.loads(json_check)

        asset_index = ''

        surface_filters = ['tileable displacement', 'surface imperfection', 'metal']

        if len(json_check['categories']) >= 1:

            if json_parse['isCustom'] == True:
                asset_index = 'Custom Surface'

            elif json_check['categories'][0].lower() == '3d' and 'scatter' not in json_check['tags']:
                asset_index = '3D Asset'

            elif json_check['categories'][0].lower() == '3d' and 'scatter' in json_check['tags']:
                asset_index = 'Scatter 3D'

            elif json_check['categories'][0].lower() == 'surface' and 'metal' in json_check['tags']:
                asset_index = 'Metal'

            elif json_check['categories'][0].lower() == 'surface' and 'surface imperfection' in json_check['tags']:
                asset_index = 'Imperfection'

            elif json_check['categories'][0].lower() == 'surface' and 'tileable displacement' in json_check['tags']:
                asset_index = 'Displacement'

            elif json_check['categories'][0].lower() == 'surface' and any(i not in surface_filters for i in json_check['tags']):
                asset_index = 'Surface'

            elif json_check['categories'][0].lower() == 'brush':
                asset_index = 'Brush'

            elif json_check['categories'][0].lower() == 'atlas' and 'decal' in json_check['tags']:
                asset_index = 'Decal'

            elif json_check['categories'][0].lower() == 'atlas' and 'decal' not in json_check['tags']:
                asset_index = 'Atlas'

            elif json_check['categories'][0].lower() == '3dplant':
                asset_index = '3D Plant'


        end_value = asset_index

        return end_value

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value)) 
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return 'Failed'
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_get_import_data outputs a readable array structure of assets containing all the data you need to import an asset.
# The function takes 0 arguments: 
#-

# Usage example ():
#ms_get_import_data()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_get_import_data():

    try:
        export_array = []
        data = None

        with open(ms_return_path() + '/megascansAsset.json') as f:
            data = f.read()

        json_array = json.loads(data)

        for js_ in json_array:

            try:
                texture_maps = []
                geo_list = []

                for item in js_['components']:
                    if 'path' in item:
                        texture_maps.append([item['path'], item['type']])

                for item in js_['meshList']:
                    if 'path' in item:
                        geo_list.append(item['path'])


                Export_ = dict({
                    "AssetID": js_['id'],
                    "Type": ms_get_asset_type(js_),
                    "FolderPath": js_['path'],
                    "FolderName": (os.path.basename(js_['path'])),
                    "MeshList": geo_list,
                    "TextureList": texture_maps,
                    "Resolution": js_['resolution'],
                })

                export_array.append(Export_)

            except Exception as e:
                print(js_)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                return []
                pass

        return export_array

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return []
        pass

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_change_node_property is used to change the property of a node inside that's inside a material.
# The function takes 4 arguments: 
#- The material's UObject
#- The node's description value (str)
#- The name of the property we want to change
#- The value of the property we want to change

# Usage example (here we're changing the value of a StaticSwitchParameter to True):

#ms_change_node_property(ue.load_object(Material, '/Game/MyBasicMaterial'), 'ms_BaseColor_Switch', 'DefaultValue', True)

# 'ms_BaseColor_Switch' corresponds to the description we've put in the StaticSwitchParameter node.
# 'DefaultValue' refers to the name of the StaticSwitchParameter's switch value
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_change_node_property(material, node_desc, property_, property_value):

    try:

        node_desc = ms_find_param(node_desc, material)
        node_desc.set_property(property_, property_value)
        node_desc.save_package()

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value)) 
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_change_material_property is used to change a material's property.
# The function takes 3 arguments: 
#- The material's path
#- The name of the value we want to change
#- The new value we want to set

# Usage example (here we're changing the ShadingModel to Unlit):

#ms_change_material_property(ue.load_object(Material, '/Game/MyBasicMaterial'), "ShadingModel", 0)

# The last argument (6) is part of the ShadingModel's options array. 0 corresponds to Unlit, and 1 which is the default
# will set it to Default Lit.

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_change_material_property(material, property_desc, property_value):

    try:

        material.set_property(property_desc, property_value)

        print("Changed material property " + str(property_desc) + "to" + str(property_value))

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value)) 
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_import_mesh is used to import an FBX or OBJ mesh.
# The function takes 2 arguments: 
#- The mesh's directory path
#- The mesh's import path (basically where you want to place in your UE4 project)

# Usage example ():

#ms_import_mesh('C:/Users/Username/Desktop/MyMesh.obj', '/Game/Mesh_Folder')

# '/Game/Mesh_Folder' means that we're saving our mesh to the "Mesh_Folder" folder inside "Content" which corresponds to "Game".


        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_import_mesh(MeshPath, AssetPath):

    try:

        fbx_factory = PyFbxFactory()

        fbx_factory.ImportUI.bCreatePhysicsAsset = False
        fbx_factory.ImportUI.bImportMaterials = False
        fbx_factory.ImportUI.bImportTextures = False
        fbx_factory.ImportUI.bImportAnimations = False
        fbx_factory.ImportUI.StaticMeshImportData.ImportUniformScale = 5.0; # This value changes the scale of the mesh on import.

        if MeshPath.lower().endswith("obj"):
            #importme_ = ue.import_asset(MeshPath, AssetPath)
            fbx_factory.ImportUI.bIsObjImport = True
            mesh_ = fbx_factory.factory_import_object(MeshPath, AssetPath)
        else:
            mesh_ = fbx_factory.factory_import_object(MeshPath, AssetPath)
            
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value)) 
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_create_material_instance creates a material instance.
# The function takes 3 arguments: 
#- The parent material's UObject
#- The new material instance's name
#- The material instance's path

# Usage example ():

#name_ = "base_material"
#ms_create_material_instance(ue.load_object(Material, '/Game/MyBasicMaterial'), name_, "/Game/Materials_Folder/" + name_)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_create_material_instance(M_Parent, Inst_Name, InstancePath):

    try:

            material_instance = ue.create_material_instance(M_Parent, InstancePath, Inst_Name)
            material_instance.save_package()

            print("Megascans Integration - Created Material Instance " + str(Inst_Name))

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_assign_texture_to_instance creates a material instance.
# The function takes 3 arguments: 
#- The material instance's path
#- The texture path
#- The property from the material instance that we want to change.

# Usage example ():

#ms_assign_texture_to_instance("/Game/Megascans", ("/Game/" + "Rubber_Albedo"), "Albedo")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_assign_texture_to_instance(path_, Texture, Property):

    try:

        material_instance = ""
        for obj_ in ue.get_assets(path_):
            try:
                if obj_.is_a(MaterialInstance):
                    material_instance = obj_
                    break
            except:
                pass
        if material_instance != "":
            Texture2D = ue.find_class('Texture2D')
            tex = ue.load_object(Texture2D, Texture)

            if tex.get_property('CompressionSettings') == 1:
                tex.set_property('bFlipGreenChannel', True)

            srgb_list = ['albedo', 'specular', 'translucency']

            if Property.lower() in srgb_list:
                tex.set_property('SRGB', True)
            else:
                tex.set_property('SRGB', False)

            material_instance.set_material_scalar_parameter(Property, 1)
            material_instance.set_material_texture_parameter(Property, tex)

            material_instance.post_edit_change()
            material_instance.save_package()

            print("Megascans Integration - Assigned texture " + str(Texture) + ' to material instance ' + str(material_instance))

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_load_asset_data imports all the available meshes from the given input path, mesh and texture format.
# The function takes 4 arguments: 
#- An str path that contains your textures and meshes to import.
#- the mesh format, which can be "fbx", "obj" or whatever format you want that is supported by ue4. 
#- the textures format, "png", "jpg" or other. 
#- An array of strings that you want to use as a mask for your naming convention. If you set custom_maps's value to None then it'll use
#- the default naming conventions (albedo, normal, roughness, ao, etc...).

# Usage example ():

# asset_path = (r"C:\Users\Username\Desktop\Pipeline_Tutorial\Door_Project").replace("\\", "/")
# pbr_maps = ["albedo", "normal", "roughness"]
# geo_array, maps_array = ms_load_asset_data(asset_path, "fbx", "png", custom_maps = pbr_maps)

# The pbr_maps array is used as a mask to get only three textures : albedo, normal and roughness. You can extend
# that list as you wish or just set custom_maps to None if your naming convention is similar to the Megascans library's.

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_load_asset_data(asset_path, mesh_frmt, texture_frmt, custom_maps = None):

    try:
        support_maps = []
        if custom_maps == None:
            support_maps = ["albedo", "normal", "roughness", "gloss",
             "specular", "metallic", "translucency", "opacity",
             "mask", "displacement", "ao", "emissive"]
        else:
            support_maps = custom_maps

        textures_array = [file_ for file_ in os.listdir(asset_path) if file_.endswith('.' + texture_frmt.lower()) and file_.split('_')[-1].split('.')[0].lower() in support_maps]
        textures_array = [(asset_path + "/" + item) for item in textures_array]

        geometry_array = [file_ for file_ in os.listdir(asset_path) if file_.lower().endswith('.' + mesh_frmt.lower())]
        geometry_array = [(asset_path + "/" + item) for item in geometry_array]

        return geometry_array, textures_array

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_apply_tex2d_to_inst creates a material instance.
# The function takes 3 arguments: 
#- The material instance's path
#- The texture path
#- The property from the material instance that we want to change.

# Usage example ():

#ms_apply_tex2d_to_inst(ue.load_object(MaterialInstance, (asset_dir + "/" + instance_name)), ("/Game/" + "Rubber_Albedo"), "Albedo")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_apply_tex2d_to_inst(mat_instance, Texture, Property):

    try:
        Texture2D = ue.find_class('Texture2D')
        tex = ue.load_object(Texture2D, Texture)

        if tex.get_property('CompressionSettings') == 1:
            tex.set_property('bFlipGreenChannel', True)

        srgb_list = ['albedo', 'specular', 'translucency']

        if Property.lower() in srgb_list:
            tex.set_property('SRGB', True)
        else:
            tex.set_property('SRGB', False)

            tex.post_edit_change()
            tex.save_package()

        mat_instance.set_material_scalar_parameter(Property, 1)
        mat_instance.set_material_texture_parameter(Property, tex)

        mat_instance.post_edit_change()
        mat_instance.save_package()

        print("Megascans Integration - Assigned texture " + str(Texture) + ' to material instance ' + str(mat_instance))

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_apply_mat_2_sel applies an input material to the currently selected actors in the scene..
# The function takes 1 arguments: 
#- The material's UObject

# Usage example ():

#ms_apply_mat_2_sel(ue.load_object(Material, '/Game/MyBasicMaterial'))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_apply_mat_2_sel(material_):

    try:
        get_sel = ue.editor_get_selected_actors()

        mesh_actors = []

        for sel in get_sel:
            try:
                if sel.is_a(StaticMeshActor):

                    print(sel.get_property('StaticMeshComponent').get_property('OverrideMaterials'))
                    sel.get_property('StaticMeshComponent').set_property('OverrideMaterials', [material_])
                    base_pos = sel.get_actor_location()
                    sel.set_actor_location(base_pos[0], base_pos[1], base_pos[2] + 0.005)
                    sel.set_actor_location(base_pos)
            except:
                pass
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_form_base_structure creates/imports all the necessary files/folders for the plugin on startup.
# The function takes 0 arguments: 
#- 

# Usage example ():

#ms_form_base_structure()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_form_base_structure():

    try:
        megascans_fldr = os.path.join(ms_return_path(),'megascans', 'ui', 'font')

        content_path = ue.get_content_dir()

        if not os.path.exists(os.path.join(content_path, 'Megascans')):
            os.mkdir(os.path.join(content_path, 'Megascans'))

        if os.path.exists(os.path.join(content_path, 'Megascans')):

            if not os.path.exists(os.path.join(content_path, 'Megascans', 'Blend_Materials')):
                os.mkdir(os.path.join(content_path, 'Megascans', 'Blend_Materials'))

            if not os.path.exists(os.path.join(content_path, 'Megascans', 'Master_Materials')):
                os.mkdir(os.path.join(content_path, 'Megascans', 'Master_Materials'))

        resources_fldr = os.path.join(ms_return_path(),'megascans', 'resources')
        mat_fldr = os.path.join(ms_return_path(),'megascans', 'materials')

        resources_ = [os.path.join(resources_fldr, file_) for file_ in os.listdir(resources_fldr) if file_.lower().endswith('.png')]
        materials_ = [file_.split('.')[0] for file_ in os.listdir(mat_fldr) if file_.lower().endswith('.json')]

        for a in resources_:
            if ms_obj_exists("/Game/Megascans/Master_Materials" + '/' + os.path.basename(a).split('.')[0]) == False:
                obj_ = ue.import_asset(a, "/Game/Megascans/Master_Materials")
                if obj_ != None:
                    obj_.save_package()

        for mat_ in materials_:
            if ms_obj_exists("/Game/Megascans/Master_Materials" + '/' + mat_) == False:
                ms_create_master_material(mat_)


    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_import_texture_list import an array of textures.
# The function takes 2 arguments: 
#- An array of paths that correspond to each texture's directory.
#- The project path in which we want to import the textures.

# Usage example ():

#ms_import_texture_list(['C:/Users/Username/Desktop/Quixel_Albedo.jpg', 'C:/Users/Username/Desktop/Quixel_Normal.jpg', 'C:/Users/Username/Desktop/Quixel_Roughness.jpg'], "/Game/TexturesFolder")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_import_texture_list(Textures, AssetPath):

    try:
        for texture in Textures:
            if ms_obj_exists(AssetPath + '/' + os.path.basename(texture).split('.')[0]) == False:
                asset = ue.import_asset(texture, AssetPath)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_create_foliage_asset creates an Unreal Foliage asset from a given listo f meshes.
# The function takes 1 arguments: 
#- A string representing the path of the asset.

# Usage example ():

#ms_create_foliage_asset("/Game/Meshes_To_Process")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_create_foliage_asset(AssetPath):

    try:

        try:
            from unreal_engine.classes import FoliageTypeFactory
        except:
            pass

        meshlist_ = ue.get_assets(AssetPath)

        for obj_ in meshlist_:
            if obj_.is_a(StaticMesh):
                factory = FoliageTypeFactory()
                foliage_type = factory.factory_create_new(AssetPath + '/Foliage/' + obj_.get_name() + '_Foliage')
                foliage_type.Mesh = ue.load_object(StaticMesh, (AssetPath + '/' + obj_.get_name()))
                foliage_type.save_package()


    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_inst_2_mesh applies a material instance to a list of meshes.
# The function takes 1 arguments: 
#- A path to the folder that contains our meshes and material instance. This value refers to a project path.

# Usage example ():

#ms_inst_2_mesh(ue.load_object(MaterialInstance, ("/Game/Content/Instance01")), ["/Game/Content/Mesh01", "/Game/Content/Mesh02", "/Game/Content/Mesh03"])

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_inst_2_mesh(inst_uobj, geo_array):

    try:
        for obj_ in geo_array:
            inst_array = [inst_uobj]

            new_settings = []
            print(obj_[0].StaticMaterials)
   
            settings = obj_[0].StaticMaterials[0].clone()
            settings.MaterialInterface = inst_array[0]
            settings.MaterialSlotName = inst_array[0].get_name()
            new_settings.append(settings)

            obj_[0].StaticMaterials = new_settings
            obj_[0].post_edit_change()
            obj_[0].save_package()

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_assign_instance_to_meshes applies a material instance to a list of meshes.
# The function takes 1 arguments: 
#- A path to the folder that contains our meshes and material instance. This value refers to a project path.

# Usage example ():

#ms_assign_instance_to_meshes("/Game/MyAssetFolder")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_assign_instance_to_meshes(AssetPath):

    try:

        MaterialInstance = ue.find_class('MaterialInstance')
        # AssetPath = ('/Game/Megascans/Wood_Board_rhkc2_2K')
        meshlist_ = ue.get_assets(AssetPath)
        instance_mat = None
        mesh_list = []

        for obj_ in meshlist_:
            if obj_.is_a(StaticMesh):
                mesh_list.append([obj_, (AssetPath + '/' + obj_.get_name())])
            elif obj_.is_a(MaterialInstance):
                instance_mat = [obj_, (AssetPath + '/' + obj_.get_name())]


        for obj_ in mesh_list:

            new_settings = []

            settings = obj_[0].StaticMaterials[0].clone()
            settings.MaterialInterface = instance_mat[0]
            settings.MaterialSlotName = instance_mat[0].get_name()
            new_settings.append(settings)

            obj_[0].StaticMaterials = new_settings

            obj_[0].save_package()

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# connect_nodes_to_material is a !DEPRECATED FUNCTION! that connects all the nodes from our material's nodes to the main node.
# The function takes 2 arguments: 
# A UObject of the material
# A string representing the material type we're targeting

# Usage example ():

# connect_nodes_to_material(material, 'Standard_MasterMaterial')

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def connect_nodes_to_material(material, material_setup):

    connections_ = [item for item in material_setup['MaterialConnections']]

    try:
        for item in connections_:
            if item.split('_')[1].lower() == 'BaseColor'.lower():
                material.BaseColor = ColorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'Metallic'.lower():
                material.Metallic = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'Normal'.lower():
                print('Found the normal ')
                material.Normal = VectorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'Roughness'.lower():
                material.Roughness = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'WorldDisplacement'.lower():
                material.WorldDisplacement = VectorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'TessellationMultiplier'.lower().lower():
                material.TessellationMultiplier = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'SpecularColor'.lower():
                material.Specular = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'EmissiveColor'.lower():
                material.EmissiveColor = ColorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'Opacity'.lower():
                material.Opacity = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'OpacityMask'.lower():
                material.OpacityMask = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'WorldPositionOffset'.lower():
                material.WorldPositionOffset = VectorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'SubsurfaceColor'.lower():
                material.SubsurfaceColor = ColorMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'AmbientOcclusion'.lower():
                material.AmbientOcclusion = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'Refraction'.lower():
                material.Refraction = ScalarMaterialInput(Expression=ms_find_param(item, material))

            elif item.split('_')[1].lower() == 'PixelDepthOffset'.lower():
                material.PixelDepthOffset = ScalarMaterialInput(Expression=ms_find_param(item, material))

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_materialblend_setup creates a texture-blended material instance. It relies on a set of selected assets in the content browser,
# where it basically gets the paths of the selected assets, then searchs for all the different texture maps in each.
# If you were to blend three megascans assets for instance, you could search for "Albedo" and select the three albeo textures that you want.
# The tool will then automatically detect all the other textures inside the albedo's folders and set up the material instance for you.

# The function takes 1 arguments: 
#- An str that is either "create" for creating a material or "update" for updating it.

# Usage example ():

#ms_materialblend_setup("create")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_materialblend_setup(input_cmd):

    material_instance = None
    blend_paths = []

    try:
        with open(ms_return_path() + '/megascans/settings.json') as f:
            settings_ = json.loads(f.read())

        actors = ue.get_selected_assets()
        if len(actors) >= 2:

            for actor in actors:
                package_name = actor.get_outer().get_name()
                blend_paths.append(os.path.dirname(package_name))

            if len(blend_paths) >= 2:
                main_f = os.path.join(ue.get_content_dir(), 'Megascans', 'Blend_Materials')
                cur_lib = len([f.path for f in os.scandir(main_f) if f.is_file() ])
                path_prefix = str(cur_lib+1) if cur_lib > 9 else "0" + str(cur_lib+1)

                obj_mat = [item for item in settings_['CustomMaterial'] if item[0].lower() == 'surface blend a'.lower()][0]
                parent_path = '/Game/Megascans/Master_Materials/' if len(obj_mat) <= 2 else obj_mat[2]
                inst_path = '/Game/Megascans/Blend_Materials'

                valid_name = (path_prefix + "_" + "Blend_Material")
                parent_mat = ue.load_object(Material, (parent_path + obj_mat[1]))

                ms_create_material_instance(parent_mat, valid_name, inst_path)

            material_instance = ue.load_object(MaterialInstance, inst_path + '/' + valid_name)
            if material_instance != 'None':
                Texture2D = ue.find_class('Texture2D')
                blend_sets = ['Base', 'R', 'G', 'B', 'A']
                blend_inputs = []

                for i in range(0, len(blend_sets)):

                    try:
                        texturepath_ = blend_paths[i]

                        requested_textures = ['albedo', 'displacement', 'roughness', 'normal']
                        for obj_ in ue.get_assets(texturepath_):
                                    try:

                                        if obj_.is_a(Texture2D):
                                            texture_name = (obj_.get_name().split('_')[-1].lower())
                                            if "lod" in texture_name.lower():
                                                texture_name = 'Normal'

                                            if texture_name.lower() in requested_textures :

                                                attr_name = obj_.get_name().split('_')[-1]
                                                if "lod" in attr_name.lower():
                                                    attr_name = 'Normal'
                                                new_ = [blend_paths[i], (blend_sets[i] + ' ' + attr_name), obj_.get_name(), obj_]
                                                if new_ not in blend_inputs:
                                                   blend_inputs.append(new_)
                                    except:
                                        pass
                    except:
                        pass

                for blend_ in blend_inputs:
                    #print('STARTED PROCESSING................')
                    Texture2D = ue.find_class('Texture2D')
                    tex = ue.load_object(Texture2D, blend_[0] + '/' + blend_[2])
                    material_instance.set_material_scalar_parameter(blend_[1], 1)
                    material_instance.set_material_texture_parameter(blend_[1], tex)

                material_instance.save_package()
                ue.sync_browser_to_assets([material_instance])

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_set_master_material saves a master material to the -/megascans/materials repository.
# The function takes 0 arguments: 
# -

# Usage example ():

# ms_set_master_material()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_set_master_material():

    try:

        material_inputs = ["BaseColor", "Metallic", "SpecularColor", 
                          "Normal", "Roughness", "EmissiveColor", "Opacity", 
                          "OpacityMask", "WorldPositionOffset", "WorldDisplacement", "TessellationMultiplier", 
                          "SubsurfaceColor", "AmbientOcclusion", "Refraction", "PixelDepthOffset", ]

        mat_ = ue.get_selected_assets()
        clip_content = app.clipboard().text()

        material_ = None

        if len(mat_) >= 1 and mat_[0].is_a(Material):
            material_ = (mat_[0])

            material_.save_package()
            material_.modify()

            ue.open_editor_for_asset(material_)

            nodes_ = material_.properties()
            input_structs = []

            for expression_ in material_.Expressions:
                if expression_.get_property('DESC').lower() in [('ms_'+item.lower()) for item in material_inputs]:
                    expression_.set_property('DESC', '')

            for node_ in material_inputs:
                expression_ = material_.get_property(node_).get_field('Expression')
                if expression_ != None:
                    input_structs.append([expression_, node_])

            for node_ in input_structs:
                node_[0].set_property('DESC', ('ms_' + node_[1]))

            ue.close_editor_for_asset(material_)
            material_.save_package()

        else:
            ue.log('Please make sure that : \n - You have a material selected in the content browser.\n - You have copied all the nodes in the material by selecting them all then CTRL+C.')

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_save_master_material saves a master material to the -/megascans/materials repository.
# The function takes 0 arguments: 
# -

# Usage example ():

# ms_save_master_material()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_save_master_material():

    try:

        material_settings = ['ShadingModel', 'MaterialDomain', 'BlendMode', 'DecalBlendMode', 
                'TwoSided', 'DitheredLODTransition', 'bEnableAdaptiveTessellation', 'bEnableCrackFreeDisplacement', 
                'D3D11TessellationMode', 'MaxDisplacement', 'DitherOpacityMask']

        material_inputs = ["BaseColor", "Metallic", "SpecularColor", 
                          "Normal", "Roughness", "EmissiveColor", "Opacity", 
                          "OpacityMask", "WorldPositionOffset", "WorldDisplacement", "TessellationMultiplier", 
                          "SubsurfaceColor", "AmbientOcclusion", "Refraction", "PixelDepthOffset", ]

        mat_ = ue.get_selected_assets()
        material_ = (mat_[0])

        input_parameters = []
        settings_parameters = []

        clip_content = app.clipboard().text()

        if len(mat_) >= 1 and mat_[0].is_a(Material) and 'begin' in clip_content.lower():

            for expression_ in material_.Expressions:
                desc_ = (expression_.get_property('DESC'))
                if (str(desc_).lower()) in [('ms_'+item.lower()) for item in material_inputs]:
                    input_parameters.append(desc_)

            for obj_ in material_settings:
                try:
                    settings_parameters.append([obj_, material_.get_property(obj_)])
                except:
                    pass

            base_struct = dict({
            "MaterialName": material_.get_name(),
            "BuildVersion": [["4.21", "4.20", "4.19", "4.18", "4.17", "4.16", "4.15"], 0]
            })
            base_struct['MaterialConnections'] = input_parameters
            base_struct['MaterialProperties'] = settings_parameters

            Export_ = json.dumps((dict(base_struct)), sort_keys=True, ensure_ascii=False, indent=2)

            file_ = open((ms_return_path() + "/megascans/materials/" + material_.get_name() + '.json'), "w+")
            file_.write(Export_)
            file_.close()

            file_ = open((ms_return_path() + "/megascans/materials/" + material_.get_name() + '.uemat'), "w+")
            file_.write(clip_content)
            file_.close()

            ue.close_editor_for_asset(material_)
            material_.save_package()

        else:
            ue.log('Please make sure that : \n - You have a material selected in the content browser.\n - You have copied all the nodes in the material by selecting them all then CTRL+C.')

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_get_all_material_properties returns all the properties it can of the input material.
# The function takes 1 arguments: 
# a UObject of the material

# Usage example ():

# ms_get_all_material_properties(material)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_get_all_material_properties(material):

    material_properties = []
    try:
        for obj_ in material.properties():
            try:
                material_properties.append([obj_, material.get_property(obj_)])
            except:
                pass

        return material_properties

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_auto_populate_foliage takes gets all Foliage assets from a given path to add them inside the current foliage editor.
# The function takes 1 arguments: 
# a str corresponding to the current path where you have Foliage assets.

# Usage example ():

# ms_auto_populate_foliage('/Game/Megascans/3D_Plants/02_semkO/Foliage')

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_auto_populate_foliage(foliage_dir):


    try:
        list_uobjects = ue.get_assets(foliage_dir)

        foliage_assets = []

        for item in list_uobjects:
            try:
                if item.is_a(FoliageType):
                    foliage_assets.append(item)
            except:
                pass

        if len(foliage_assets) >= 1:
            # print(foliage_assets[0].get_property('IsSelected'))
            current_world = ue.get_editor_world()
            for f_asset in foliage_assets:
                f_asset.set_property('IsSelected', True)
                current_world.add_foliage_asset(f_asset)
            print("Populated " + str(len(foliage_assets)) + " assets in the foliage editor.")

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_create_master_material creates a master material from the given material type.
# A material type is a material that runs on a specific set of megascans objects.
# For instance, the Foliage_MasterMaterial has an array of ['3dplant', 'atlas'] which makes it only appliable on those two.

# The function takes 1 arguments: 
# a string of the material type. The material types are written by the IntegrationToBridge_Format function.

# Usage example ():

# ms_create_master_material('Standard_MasterMaterial')

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_create_master_material(MaterialType):

    try:

        material = None
        material_setup = json.load(open(ms_return_path() + "/megascans/materials/" + MaterialType + '.json'))

        package_name = ('/Game/Megascans/Master_Materials/' + material_setup['MaterialName'])

        # read the material data
        mat_data = None
        with open(ms_return_path() + "/megascans/materials/" + material_setup['MaterialName'] + '.uemat') as f:
            mat_data = f.read()

        # set a new material factory

        factory = MaterialFactoryNew()
        # set the material path

        # create the material
        material = factory.factory_create_new(package_name)

        # open the material editor
        ue.open_editor_for_asset(material)

        clipboard.copy(mat_data) #Double-check measure that copies the material's content into the clipboard

        # copy mat_data to the clipboard
        ue.clipboard_copy(mat_data)

        # get material graph, then paste the clipboard content into it
        ue.open_editor_for_asset(material)
        graph = material.get_material_graph()
        FMaterialEditorUtilities.paste_nodes_here(graph, (-2000, 0))
        FMaterialEditorUtilities.update_material_after_graph_change(graph)

        # this will build a whole new material
        FMaterialEditorUtilities.command_apply(material)

        material = ue.load_object(Material, package_name)
        material.save_package()

        material.modify()

        for param_ in material_setup['MaterialProperties']:
            val = param_[1]
            if param_[1] == 'true':
                val = True
            elif param_[1] == 'false':
                val = False

            material.set_property(param_[0], val)

        connect_nodes_to_material(material, material_setup)

        material.post_edit_change()
        material.save_package()

        clipboard.copy("") #Clear the clipboard

        ue.close_editor_for_asset(material)
        ue.close_editor_for_asset(material)

        return material

    except Exception as e:
        return None
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value))
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ms_base_importer provides a basic importer that relies on the Bridge's livelink.
# Whenever a new asset is sent from the Bridge this is the function that gets called to deal with it, from setting
# up the import data to having everything right inside the engine.

# The function takes 1 arguments: 
#- 

# Usage example ():

#ms_base_importer(ue.load_object()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ms_base_importer():

    try:
        ms_form_base_structure()

        base_maps = ['albedo', 'normal', 'displacement', 'opacity', 'translucency']

        pbr_specular = base_maps + ['specular', 'gloss', 'brush', 'mask']
        pbr_metallic = base_maps + ['roughness', 'metalness', 'brush', 'mask']

        with open(ms_return_path() + '/megascans/settings.json') as f:
            settings_ = json.loads(f.read())

        Assets_Array = ms_get_import_data()

        for obj_ in Assets_Array:

            try:
                os.mkdir(os.path.join(ue.get_content_dir(), "Megascans", obj_['Type'].replace(' ', '_')))
            except:
                pass

            obj_mat = [item for item in settings_['CustomMaterial'] if obj_['Type'].lower() == item[0].lower()][0]

            main_f = os.path.join(ue.get_content_dir(), 'Megascans', obj_['Type'].replace(' ', '_'))
            cur_lib = len([f.path for f in os.scandir(main_f) if f.is_dir() ])
            path_prefix = str(cur_lib+1) if cur_lib > 9 else "0" + str(cur_lib+1)


            asset_name = (path_prefix + "_" + obj_['FolderName'].replace(' ', '_'))
            content_dir = ("/Game/Megascans/" + obj_['Type'].replace(' ', '_') + "/" + asset_name)
            instance_name = (asset_name +  '_' + obj_['Resolution'] + '_inst')

            pbr_workflow = pbr_metallic if settings_['PBR Workflow'].lower() == 'metallic' else pbr_specular

            geo_array, maps_array = obj_['MeshList'], obj_['TextureList']

            maps_array = [item[0] for item in maps_array if ms_get_map(os.path.basename(item[0])).lower() in pbr_workflow]

            if len(maps_array) >= 1:

                if len(geo_array) >= 1:
                    for item in geo_array:
                        ms_import_mesh(item, content_dir)
                if len(maps_array) >= 1:
                    ms_import_texture_list(maps_array, content_dir)

                if obj_['Type'] == '3D Plant' or obj_['Type'] == 'Scatter 3D':
                    print('Foliage asset detected, creating foliage...')
                    ms_create_foliage_asset(content_dir)

                if ms_instance_exists(content_dir + "/" + instance_name) == False:
                    parent_path = '/Game/Megascans/Master_Materials/' if len(obj_mat) <= 2 else obj_mat[2]
                    parent_mat = ue.load_object(Material, parent_path + obj_mat[1])
                    ms_create_material_instance(parent_mat, instance_name, content_dir)

                inst_uobj = ue.load_object(MaterialInstance, content_dir + "/" + instance_name)

                static_mesh_array = [[item, (content_dir + '/' + item.get_name())] for item in ue.get_assets(content_dir) if item.is_a(StaticMesh)]

                if len(geo_array) >= 1:
                    ms_inst_2_mesh(inst_uobj, static_mesh_array)

                for texture in [item for item in ue.get_assets(content_dir) if item.is_a(Texture2D)]:
                    try:
                        text_input = ms_get_map(texture.get_name())
                        if text_input.lower() == 'metalness':
                            text_input = 'metallic'
                        text_path = texture.get_path_name()
                        ms_apply_tex2d_to_inst(inst_uobj, text_path, text_input)
                    except:
                        pass

                if obj_['Type'] == '3D Plant' or obj_['Type'] == 'Scatter 3D' and settings_['AutoFoliage'] == 1:
                    ms_auto_populate_foliage((content_dir + '/Foliage').replace('//', '/'))

                if settings_['Surface2Selection'] == 1 and obj_['Type'] == 'Surface' or obj_['Type'] == 'Custom Surface':
                    ms_apply_mat_2_sel(inst_uobj)

                ue.sync_browser_to_assets(ue.get_assets(content_dir))

            else:
                ue.message_dialog_open(0, 'No textures maps were found for import, operation cancelled.')

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(' Error Info : ' + str(exc_value)) 
        print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def ms_ticker_loop(delta_time):
    try:
        loop.stop()
        loop.run_forever()
    except Exception as e:
        ue.log_error(e)
    return True

def ms_bridge_listener_cancel():
    try:
        for task in asyncio.Task.all_tasks():
                task.cancel()
    except:
        pass


async def ms_simple_timer(frequency):
    while True:
        try:
            await asyncio.sleep(frequency)

            material_setup = json.load(open(ms_return_path() + '/megascansAsset.json'))

            if material_setup != '' and len(material_setup) >= 1:
                ue.log("Imported " + str(len(material_setup)) + " assets from Megascans Bridge")
                ms_base_importer()
                material_setup = []

                try:
                    with open(ms_return_path() + '/megascansAsset.json', 'w') as outfile:
                        json.dump(material_setup, outfile)
                except:
                    pass

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(' Error Info : ' + str(exc_value))
            #print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            #print("Encountered error during asyncIO listener, closing port...")
            #break
            pass

# ms_import_standard()

# ms_bridge_listener_cancel()

# print("Starting Bridge Listener...")

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)

# ticker = ue.add_ticker(ms_ticker_loop)

# asyncio.ensure_future(ms_simple_timer(1))