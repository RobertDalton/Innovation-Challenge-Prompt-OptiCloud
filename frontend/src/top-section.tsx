import { Flex, IconButton } from '@chakra-ui/react';
import { Tooltip } from '@/components/ui/tooltip';
import { Avatar } from '@/components/ui/avatar';

import { useSidebarContext } from './sidebar-context';

import { ModelsMenu } from './ModelsMenu';

import { NewChatIcon, SidebarIcon } from './icons/sidebar-icons';

export function TopSection() {
  const { sideBarVisible, toggleSidebar } = useSidebarContext();

  return (
    <Flex justify="space-between" align="center" p={2}>
      {!sideBarVisible && (
        <Flex>
          <Tooltip
            content="Close sidebar"
            positioning={{ placement: 'right' }}
            showArrow
          >
            <IconButton
              variant="ghost"
              onClick={() => {
                toggleSidebar();
              }}
            >
              <SidebarIcon fontSize="2xl" color="white" />
            </IconButton>
          </Tooltip>

          <Tooltip content="New chat" showArrow>
            <IconButton
              variant="ghost"
              onClick={() => {
                alert('New chat');
              }}
            >
              <NewChatIcon fontSize="2xl" color="white" />
            </IconButton>
          </Tooltip>
          <ModelsMenu />
        </Flex>
      )}

      {sideBarVisible && <ModelsMenu />}

      <Avatar
        name="Josue"
        size="sm"
        colorPalette="teal"
        variant="solid"
        mr={3}
      />
    </Flex>
  );
}
