import React, { memo, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { Grid, OrbitControls, Environment, GizmoHelper, GizmoViewport, Html } from '@react-three/drei'
import { useControls } from 'leva'
import { Text } from '@react-three/drei'
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
      camera={{ position: [0, 40, 40], fov: 25 }}
      style={{ height: '100%', width: '100%' }}
    >
      <Grid
        position={[0, 0, 0]}
        rotation={[0, 0, 0]} // Rotate from XY to XZ
        args={gridSize}
        sectionSize={gridConfig.sectionSize}
        sectionThickness={gridConfig.sectionThickness}
        sectionColor={gridConfig.sectionColor}
        fadeDistance={gridConfig.fadeDistance}
        fadeStrength={gridConfig.fadeStrength}
        followCamera={gridConfig.followCamera}
        infiniteGrid={true} // 🔥 Force manual orientation
        renderOrder={0}
      />

      {/* Axis Labels */}
      <Text position={[2, 0, 0]} fontSize={0.5} color="red">
        X
      </Text>
      <Text position={[0, 2, 0]} fontSize={0.5} color="green">
        Y
      </Text>
      <Text position={[0, 0, 2]} fontSize={0.5} color="blue">
        Z
      </Text>


      <group position={[0, 0, 0]}>
        {/* Tower Elements */}
        {elements.map((section, idx) => (
          <group key={`section-${idx}`}>
            {section.elements.map((el, i) => {
              const geometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(...el.node_i),
                new THREE.Vector3(...el.node_j)
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

        {/* Tower Nodes */}
        {coordinates.map((coord, index) =>
          Object.entries(coord).map(([key, val]) =>
            Array.isArray(val) ? (
              <mesh
                key={`${index}-${key}`}
                position={[val[0], val[1], val[2]]}
                renderOrder={3}
                onClick={(e) => {
                  e.stopPropagation()
                  if (
                    selectedNode?.x === val[0] &&
                    selectedNode?.y === val[1] &&
                    selectedNode?.z === val[2]
                  ) {
                    setSelectedNode(null)
                  } else {
                    setSelectedNode({ x: val[0], y: val[1], z: val[2], key })
                  }
                }}
              >
                <sphereGeometry args={[0.08, 8, 8]} />
                <meshStandardMaterial color="red" depthTest={false} />

                {selectedNode?.x === val[0] &&
                  selectedNode?.y === val[1] &&
                  selectedNode?.z === val[2] && (
                    <Html
                      distanceFactor={10}
                      style={{ pointerEvents: 'none', color: 'white', fontSize: '12px' }}
                    >
                      {selectedNode.key} (
                      {selectedNode.x.toFixed(2)}, {selectedNode.y.toFixed(2)}, {selectedNode.z.toFixed(2)})
                    </Html>
                  )}
              </mesh>
            ) : null
          )
        )}
      </group>

      <OrbitControls
        makeDefault
        enableRotate={true}
        enableZoom={true}
        enablePan={true}
        target={[0, 20, 0]}
      />

      <Environment preset="city" />

      <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
        <GizmoViewport axisColors={['#ff4d4d', '#4dff4d', '#4d4dff']} labelColor="white" />
      </GizmoHelper>
    </Canvas>
  )
}

export default memo(TowerPlot)
