import React, { memo, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { Grid, OrbitControls, Environment, GizmoHelper, GizmoViewport, Html } from '@react-three/drei'
import { useControls } from 'leva'
import * as THREE from 'three'

const TowerPlot = ({ coordinates = [], elements = [] }) => {
  const [selectedNode, setSelectedNode] = useState(null)

  const { gridSize, lineThickness, ...gridConfig } = useControls({
    gridSize: [10.5, 10.5],
    sectionSize: { value: 3.3, min: 0, max: 10, step: 0.1 },
    sectionThickness: { value: 1.5, min: 0, max: 5, step: 0.1 },
    sectionColor: '#575d9b',
    lineThickness: { value: 4, min: 1, max: 10, step: 1 },
    fadeDistance: { value: 25, min: 0, max: 100, step: 1 },
    fadeStrength: { value: 1, min: 0, max: 1, step: 0.1 },
    followCamera: false,
    infiniteGrid: true
  })

  return (
    <Canvas
      shadows
      camera={{ position: [0, 40, 0], fov: 25 }}
      style={{ height: '100%', width: '100%' }}
      onCreated={({ camera }) => {
        camera.up.set(0, 0, 1)
        camera.lookAt(0, 0, 0)
      }}
    >
      <Grid
        position={[0, 0, -1]}
        args={gridSize}
        sectionSize={gridConfig.sectionSize}
        sectionThickness={gridConfig.sectionThickness}
        sectionColor={gridConfig.sectionColor}
        fadeDistance={gridConfig.fadeDistance}
        fadeStrength={gridConfig.fadeStrength}
        followCamera={gridConfig.followCamera}
        infiniteGrid={gridConfig.infiniteGrid}
        renderOrder={0}
      />

      <group position={[0, 0, 0]} rotation={[0, Math.PI, 0]}>
        {elements.map((section, idx) => (
          <group key={`section-${idx}`}>
            {section.elements.map((el, i) => {
              const geometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(el.node_i[0], 0, -el.node_i[1]),
                new THREE.Vector3(el.node_j[0], 0, -el.node_j[1])
              ])
              const color = idx % 2 === 0 ? '#ff0000' : '#ffffff'
              return (
                <line key={`el-${i}`} geometry={geometry} renderOrder={2}>
                  <lineBasicMaterial attach="material" color={color} linewidth={lineThickness} depthTest={false} />
                </line>
              )
            })}
          </group>
        ))}

        {coordinates.map((coord, index) =>
          Object.entries(coord).map(([key, val]) =>
            Array.isArray(val) ? (
              <mesh
              key={`${index}-${key}`}
              position={[val[0], 0, -val[1]]}
              renderOrder={3}
              onClick={(e) => {
                e.stopPropagation()
                if (selectedNode?.x === val[0] && selectedNode?.y === -val[1]) {
                  setSelectedNode(null)
                } else {
                  setSelectedNode({ x: val[0], y: -val[1], key })
                }
              }}
            >
              <sphereGeometry args={[0.08, 8, 8]} />
              <meshStandardMaterial color="red" depthTest={false} />

              {selectedNode?.x === val[0] && selectedNode?.y === -val[1] && (
                <Html distanceFactor={10} style={{ pointerEvents: 'none', color: 'white', fontSize: '12px' }}>
                  {selectedNode.key} ({selectedNode.x.toFixed(2)}, {selectedNode.y.toFixed(2)})
                </Html>
              )}
            </mesh>

            ) : null
          )
        )}
      </group>

      <OrbitControls makeDefault enableRotate={false} enableZoom={true} enablePan={true} target={[0, 0, 0]} />
      <Environment preset="city" />
      <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
        <GizmoViewport axisColors={['#9d4b4b', '#2f7f4f', '#3b5b9d']} labelColor="white" />
      </GizmoHelper>
    </Canvas>
  )
}

export default memo(TowerPlot)
