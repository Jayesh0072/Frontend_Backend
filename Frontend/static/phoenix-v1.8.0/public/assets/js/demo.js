(function (factory) {
  typeof define === 'function' && define.amd ? define(factory) :
  factory();
})((function () { 'use strict';

  const { config } = window.config;
  const { pathname } = window.location;

  console.log(pathname, config);

  Object.keys(config).forEach(key => {
    localStorage.setItem(key, config[key]);
  });

  document.documentElement.classList.remove('dark');

  const navbarTop = document.querySelector('.navbar-top');
  const navbarVertical = document.querySelector('.navbar-vertical');
  console.log(pathname.includes('/demo/dark-mode.html'));

  if (pathname.includes('/demo/dark-mode.html')) {
    localStorage.setItem('phoenixTheme', 'dark');
    document.documentElement.classList.add('dark');
  }

  if (pathname.includes('/demo/darknav.html')) {
    localStorage.setItem('phoenixNavbarVerticalStyle', 'darker');
    localStorage.setItem('phoenixNavbarTopStyle', 'darker');
    navbarTop.classList.add('navbar-darker');
    navbarVertical.classList.add('navbar-darker');
  }

  if (pathname.includes('/demo/sidenav-collapse.html')) {
    localStorage.setItem('phoenixIsNavbarVerticalCollapsed', 'true');
    document.documentElement.classList.add('navbar-vertical-collapsed');
  }

  if (pathname.includes('/demo/navbar-top-slim.html')) {
    localStorage.setItem('phoenixNavbarTopShape', 'slim');
    localStorage.setItem('phoenixNavbarPosition', 'horizontal');
    // document.documentElement.classList.add('navbar-vertical-collapsed');
  }

  if (pathname.includes('/demo/navbar-top.html')) {
    document.documentElement.classList.add('navbar-horizontal');
  }

  if (pathname.includes('/demo/topnav-slim.html')) {
    localStorage.setItem('phoenixNavbarTopShape', 'slim');
  }

  if (pathname.includes('/demo/horizontal-slim.html')) {
    localStorage.setItem('phoenixNavbarTopShape', 'slim');
    localStorage.setItem('phoenixNavbarPosition', 'horizontal');
  }

}));
//# sourceMappingURL=demo.js.map
