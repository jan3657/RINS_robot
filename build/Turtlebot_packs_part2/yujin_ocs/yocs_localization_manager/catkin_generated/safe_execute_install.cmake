execute_process(COMMAND "/home/team_beta/Rins/build/Turtlebot_packs_part2/yujin_ocs/yocs_localization_manager/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/team_beta/Rins/build/Turtlebot_packs_part2/yujin_ocs/yocs_localization_manager/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
