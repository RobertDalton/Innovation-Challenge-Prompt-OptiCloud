import { Box, Flex, Input, Span, Stack } from '@chakra-ui/react';
import {
  Center,
  Circle,
  Heading,
  HStack,
  IconButton,
  Link,
  Text,
  VStack,
} from '@chakra-ui/react';
import { NewChatIcon, SidebarIcon, SmallGPTIcon } from './icons/sidebar-icons';
import { Tooltip } from './components/ui/tooltip';
import { ModelsMenu } from './ModelsMenu';
import { Avatar } from './components/ui/avatar';
import { InputGroup } from './components/ui/input-group';
import {
  FileUploadList,
  FileUploadRoot,
  FileUploadTrigger,
} from './components/ui/file-upload';
import { CgAttachment } from 'react-icons/cg';
import { BsSendFill } from 'react-icons/bs';
import { Button } from './components/ui/button';

interface PromptButtomProps {
  icon?: React.ReactElement;
  description: string;
}

function PromptButtom(props: PromptButtomProps) {
  const { icon, description } = props;
  return (
    <Button variant="outline" size="sm" borderRadius="full">
      {icon} <Span color="fg.subtle">{description}</Span>
    </Button>
  );
}

function App() {
  return (
    <Flex minH="100vh">
      <Box bg="bg.muted" w="260px">
        <Stack h="full" px={3} py={2}>
          <Flex justify="space-between">
            <Tooltip
              content="Close sidebar"
              positioning={{ placement: 'right' }}
              showArrow
            >
              <IconButton
                backgroundColor="bg.muted"
                onClick={() => {
                  alert('Close sidebar');
                }}
              >
                <SidebarIcon fontSize="2xl" color="white" />
              </IconButton>
            </Tooltip>

            <Tooltip content="New chat" showArrow>
              <IconButton
                backgroundColor="bg.muted"
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

      <Box flex={1}>
        <Stack h="full">
          <Flex justify="space-between" align="center" p={2}>
            <ModelsMenu />
            <Avatar
              name="Josue"
              size="sm"
              colorPalette="teal"
              variant="solid"
              mr={3}
            />
          </Flex>

          <Center flex={1}>
            <VStack gap={6}>
              <Heading size="3xl">
                What prompt can I help you to improve?
              </Heading>
              <Center>
                <InputGroup
                  minW="768px"
                  startElement={
                    <FileUploadRoot>
                      <FileUploadTrigger asChild>
                        <Button variant="ghost" size="sm">
                          <CgAttachment fontSize="2xl" color="fg" />
                        </Button>
                      </FileUploadTrigger>
                      <FileUploadList />
                    </FileUploadRoot>
                  }
                  endElement={
                    <IconButton fontSize="2xl" size="sm" borderRadius="full">
                      <BsSendFill fontSize="2xl" />
                    </IconButton>
                  }
                >
                  <Input
                    placeholder="Improve Your Prompt Here"
                    variant="subtle"
                    size="lg"
                    borderRadius="full"
                    mx={3}
                  />
                </InputGroup>
              </Center>

              <HStack>
                <PromptButtom
                  icon={<SmallGPTIcon fontSize="lg" />}
                  description="Improve prompt 1"
                />
                <PromptButtom
                  icon={<SmallGPTIcon />}
                  description="Improve prompt 2"
                />
                <PromptButtom
                  icon={<SmallGPTIcon />}
                  description="Improve prompt 3"
                />
                <PromptButtom description="More" />
              </HStack>
            </VStack>
          </Center>

          <Box pb={2}>
            <Center fontSize="xs" color="fg.muted">
              OptiCloud @ 2025
            </Center>
          </Box>
        </Stack>
      </Box>
    </Flex>
  );
}

export default App;
