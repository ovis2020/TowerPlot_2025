import React, { useEffect, useRef } from "react";
import * as THREE from "three";

const Tower3D = ({ towerData }) => {
    const mountRef = useRef(null);

    useEffect(() => {
        if (!towerData) return;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, 500);
        mountRef.current.appendChild(renderer.domElement);

        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
        let yOffset = 0;

        towerData.Segments.forEach(segment => {
            const geometry = new THREE.BoxGeometry(segment.base_width, segment.height, segment.base_width);
            const cube = new THREE.Mesh(geometry, material);
            cube.position.y = yOffset + segment.height / 2;
            scene.add(cube);
            yOffset += segment.height;
        });

        camera.position.z = 10;

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    }, [towerData]);

    return <div ref={mountRef}></div>;
};

export default Tower3D;
