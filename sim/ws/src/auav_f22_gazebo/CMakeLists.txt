cmake_minimum_required(VERSION 3.5)
project(auav_f22_gazebo)

find_package(ignition-gazebo6 REQUIRED)

find_package(ament_cmake REQUIRED)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

#-----------#
# Functions #
#-----------#

function(glob_generate target file_glob)
  file(READ .gitignore gitignore_content)
  file(GLOB_RECURSE glob_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${file_glob})
	set(gen_files)
	foreach(glob_file ${glob_files})
		string(REGEX REPLACE "\\.[^.]*$" "" file_name ${glob_file})
		string(REGEX MATCH "[^.]*$" file_ext ${glob_file})
		get_filename_component(file_dir ${glob_file} DIRECTORY)
		set(in_file ${CMAKE_CURRENT_SOURCE_DIR}/${glob_file})
		file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${file_dir})
		set(out_file ${CMAKE_CURRENT_SOURCE_DIR}/${file_name})
		string(REGEX REPLACE ".sdf" ".sdf" out_file ${out_file})
		if (${file_ext} STREQUAL "jinja")
			if(GENERATE_ROS_MODELS)
				add_custom_command(OUTPUT ${out_file}
        	                	COMMAND
                	                        ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/jinja_gen.py ${in_file} ${CMAKE_CURRENT_SOURCE_DIR} --generate_ros_models true
                        	        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/jinja_gen.py ${in_file}
                                	VERBATIM
	                                )
			else()
				add_custom_command(OUTPUT ${out_file}
	                                COMMAND
        	                                ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/jinja_gen.py ${in_file} ${CMAKE_CURRENT_SOURCE_DIR}
                	                DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/jinja_gen.py ${in_file}
                        	        VERBATIM
                                	)
			endif()
			list(APPEND gen_files_${target} ${out_file})
			string(REGEX REPLACE "${CMAKE_CURRENT_SOURCE_DIR}/" "" gitignore_str ${in_file})
			string(REGEX REPLACE ".jinja" "" gitignore_str ${gitignore_str})
			string(FIND ${gitignore_content} ${gitignore_str} gitignore_substr)
			if(${gitignore_substr} EQUAL -1)
				file(APPEND .gitignore ${gitignore_str} "\n")
			endif()
		endif()
	endforeach()
	add_custom_target(${target} ALL DEPENDS ${gen_files_${target}})
endfunction()

glob_generate(models_gen ${CMAKE_CURRENT_SOURCE_DIR}/models/*.jinja)
glob_generate(worlds_gen ${CMAKE_CURRENT_SOURCE_DIR}/worlds/*.jinja)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY
    #ign
    launch
    models
    rviz
    worlds
  DESTINATION
    share/${PROJECT_NAME}/
)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/${PROJECT_NAME}.dsv.in")

ament_package()
