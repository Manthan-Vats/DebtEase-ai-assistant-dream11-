import { Application } from 'https://unpkg.com/@splinetool/runtime';

const iframe = document.getElementById('splineCanvas');
const canvas = document.createElement('canvas');
iframe.parentNode.insertBefore(canvas, iframe);
iframe.style.display = 'none';

const spline = new Application(canvas);

spline.load(iframe.src).then(() => {
  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = -(e.clientY / window.innerHeight - 0.5) * 2;

    // Replace 'Head' with the actual object name from Spline
    const head = spline.findObjectByName('Head');

    if (head) {
      head.rotation.y = x * 0.5; // turn head left/right
      head.rotation.x = y * 0.5; // look up/down
    }
  });
});
