import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
/* -------------------------------------------------------------------------- */
/*                                  Count Up                                  */
/* -------------------------------------------------------------------------- */

const showcaseParallaxInit = () => {
  const { getData } = window.phoenix.utils;
  const elements = document.querySelectorAll('[data-gsap]');

  if (elements) {
    Array.from(elements).forEach(el => {
      const val = getData(el, 'gsap');
      gsap.to(el, {
        y: val,
        ease: 'none',
        scrollTrigger: {
          trigger: '.gsap',
          scrub: true,
          start: '+=450 bottom',
          toggleActions: 'play none none reverse'
        }
      });
    });
  }
};

export default showcaseParallaxInit;
