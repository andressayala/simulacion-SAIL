from dm_control import mjcf

import numpy as np

from gymnasium import spaces
import gymnasium as gym

import mujoco.viewer

import time 

def make_boat(model, pos=[0, 0]):

  model.asset.add('mesh', name='Hull', file='Hull.stl')
  model.asset.add('mesh', name='Rudder', file='Rudder.stl')

  boat = model.worldbody.add('body', name='Boat', pos=np.hstack([pos, [0.2]]))
  boat.add('geom', type='mesh', mesh='Hull', fluidshape='ellipsoid')
  boat.add('joint', name='x', type='slide', axis=[1, 0, 0])
  boat.add('joint', name='y', type='slide', axis=[0, 1, 0])
  boat.add('joint', name='z', type='hinge', axis=[0, 0, 1])
  boat.add('camera', name='cam', pos=[0,-0.5, 0.2], mode='targetbody', target='Boat')

  rudder = boat.add('body', name='Rudder', pos=[-0.029536, -0.251494, 0.033548])
  rudder.add('geom', type='mesh', mesh='Rudder')
  rudder.add('joint', name='Rudder Joint', type='hinge', axis=[0, 0, 1], range=[-90, 90])
  rudder.add('site', name='motor', pos=[0, -0.027, -0.04])


  model.actuator.add('motor', name='Motor Actuator', site='motor', gear=[0, 1, 0, 0, 0, 0], ctrlrange=[-1, 1])
  model.actuator.add('position', name='Rudder Actuator', joint='Rudder Joint', kp=0.01, kv=0.0001, ctrlrange=np.deg2rad([-90, 90]))

  return model

def make_model():
  model = mjcf.RootElement()

  chequered_texture = model.asset.add('texture', type='2d', builtin='checker', width=300, height=300,
                                      rgb1=[.2, .3, .4], rgb2=[.3, .4, .5])

  grid_material = model.asset.add('material', name='Grid', texture = chequered_texture, texrepeat=[50, 50], reflectance=.2)

  model.option.density = 1000
  model.option.viscosity = 0.0009

  model.worldbody.add('light', directional=True, diffuse=[.9, .9, .9], specular=[.1, .1, .1], pos=[0, 0, 5], dir=[0, 0, -1], castshadow=True)

  model.worldbody.add('geom', type='plane', size=[0, 0, .1], material=grid_material)
  model.worldbody.add('geom', type='box', size=[0.5,0.5,0.5])

  make_boat(model, pos=[10,10])

  return model




model = make_model()
physics = mjcf.Physics.from_mjcf_model(model)

mj_model = physics.model.ptr
mj_data = physics.data.ptr

with mujoco.viewer.launch_passive(mj_model, mj_data) as viewer:
    
    
    while viewer.is_running():
        start = time.time()

        #action = env.action_space.sample()   
        #state, reward, terminated, truncated, info = env.step(action)

        physics.step()

    
        viewer.sync()