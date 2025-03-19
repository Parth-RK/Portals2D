# FindBox2D.cmake
# Locate Box2D library
# This module defines
# BOX2D_LIBRARY, the name of the library to link against
# BOX2D_FOUND, if false, do not try to link to Box2D
# BOX2D_INCLUDE_DIR, where to find Box2D headers
#
# Created by Erin Catto (original Box2D author)
# Modified for better cross-platform support

IF(NOT BOX2D_INCLUDE_DIR)
  FIND_PATH(BOX2D_INCLUDE_DIR Box2D/Box2D.h
    HINTS
    $ENV{BOX2DDIR}
    PATH_SUFFIXES include
    PATHS
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local
    /usr
    /sw # Fink
    /opt/local # DarwinPorts
    /opt/csw # Blastwave
    /opt
  )
  
  # If not found, try without the Box2D/ prefix
  IF(NOT BOX2D_INCLUDE_DIR)
    FIND_PATH(BOX2D_INCLUDE_DIR box2d.h
      HINTS
      $ENV{BOX2DDIR}
      PATH_SUFFIXES include
      PATHS
      ~/Library/Frameworks
      /Library/Frameworks
      /usr/local
      /usr
      /sw # Fink
      /opt/local # DarwinPorts
      /opt/csw # Blastwave
      /opt
    )
    
    IF(BOX2D_INCLUDE_DIR)
      # Create backward compatibility with Box2D/Box2D.h style includes
      IF(NOT EXISTS ${BOX2D_INCLUDE_DIR}/Box2D)
        message(STATUS "Creating Box2D compatibility include directory")
        file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/include/Box2D)
        file(GLOB BOX2D_HEADERS ${BOX2D_INCLUDE_DIR}/*.h)
        foreach(HEADER ${BOX2D_HEADERS})
          get_filename_component(HEADER_NAME ${HEADER} NAME)
          configure_file(${HEADER} ${CMAKE_BINARY_DIR}/include/Box2D/${HEADER_NAME} COPYONLY)
        endforeach()
        set(BOX2D_INCLUDE_DIR ${CMAKE_BINARY_DIR}/include)
      ENDIF()
    ENDIF()
  ENDIF()
ENDIF()

SET(BOX2D_FIND_COMPONENTS
  Box2D
  box2d
  Box2d
)

SET(BOX2D_LIB_NAMES
  Box2D
  box2d
  Box2d
)

FOREACH(COMPONENT ${BOX2D_FIND_COMPONENTS})
  FIND_LIBRARY(BOX2D_LIBRARY_${COMPONENT}
    NAMES ${BOX2D_LIB_NAMES}
    HINTS
    $ENV{BOX2DDIR}
    PATH_SUFFIXES lib64 lib
    PATHS
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local
    /usr
    /sw
    /opt/local
    /opt/csw
    /opt
  )
  
  IF(BOX2D_LIBRARY_${COMPONENT})
    SET(BOX2D_LIBRARY ${BOX2D_LIBRARY_${COMPONENT}})
    SET(BOX2D_FOUND TRUE)
    BREAK()
  ENDIF()
ENDFOREACH()

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Box2D DEFAULT_MSG BOX2D_LIBRARY BOX2D_INCLUDE_DIR)

MARK_AS_ADVANCED(BOX2D_INCLUDE_DIR BOX2D_LIBRARY)
