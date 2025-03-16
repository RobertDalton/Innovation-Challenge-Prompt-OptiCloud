import {
  Box,
  Circle,
  Flex,
  HStack,
  IconButton,
  Link,
  Stack,
  Text,
} from '@chakra-ui/react';
import { Tooltip } from '@/components/ui/tooltip';

import { useSidebarContext } from './sidebar-context';

import { NewChatIcon, SidebarIcon, SmallGPTIcon } from './icons/sidebar-icons';

export function Sidebar() {
  const { sideBarVisible, toggleSidebar } = useSidebarContext();

  return (
    <Box
      bg="bg.muted"
      w={!sideBarVisible ? '0' : '260px'}
      overflow="hidden"
      transition="width 0.3s"
    >
      <Stack h="full" px={3} py={2}>
        <Flex justify="space-between">
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
        </Flex>

        <Stack px={2} gap={0}>
          {/* for loop of all enhance prompts */}
          <HStack
            _hover={{ layerStyle: 'fill.muted', textDecor: 'none' }}
            px={1}
            h={10}
            borderRadius="lg"
            w="100%"
            whiteSpace="nowrap"
          >
            <Link href="#" variant="plain" _hover={{ textDecor: 'none' }}>
              <Circle size={6} bg="bg" borderWidth={1}>
                <SmallGPTIcon fontSize="md" />
              </Circle>
              <Text fontSize="sm" fontWeight="medium">
                Enhance Prompt 1
              </Text>
            </Link>
          </HStack>

          <HStack
            _hover={{ layerStyle: 'fill.muted', textDecor: 'none' }}
            px={1}
            h={10}
            borderRadius="lg"
            w="100%"
            whiteSpace="nowrap"
          >
            <Link href="#" variant="plain" _hover={{ textDecor: 'none' }}>
              <Circle size={6} bg="bg" borderWidth={1}>
                <SmallGPTIcon fontSize="md" />
              </Circle>
              <Text fontSize="sm" fontWeight="medium">
                Enhance Prompt 2
              </Text>
            </Link>
          </HStack>

          <HStack
            _hover={{ layerStyle: 'fill.muted', textDecor: 'none' }}
            px={1}
            h={10}
            borderRadius="lg"
            w="100%"
            whiteSpace="nowrap"
          >
            <Link href="#" variant="plain" _hover={{ textDecor: 'none' }}>
              <Circle size={6} bg="bg" borderWidth={1}>
                <SmallGPTIcon fontSize="md" />
              </Circle>
              <Text fontSize="sm" fontWeight="medium">
                Enhance Prompt 3
              </Text>
            </Link>
          </HStack>
        </Stack>
      </Stack>
    </Box>
  );
}
