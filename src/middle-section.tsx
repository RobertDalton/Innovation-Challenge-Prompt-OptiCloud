import { useState } from 'react';
import {
  Center,
  Heading,
  HStack,
  IconButton,
  Input,
  VStack,
  Span,
} from '@chakra-ui/react';
import { InputGroup } from '@/components/ui/input-group';
import { Button } from '@/components/ui/button';
import {
  FileUploadList,
  FileUploadRoot,
  FileUploadTrigger,
} from '@/components/ui/file-upload';

import { CgAttachment } from 'react-icons/cg';
import { BsSendFill } from 'react-icons/bs';
import { SmallGPTIcon } from './icons/sidebar-icons';

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

export function MiddleSection() {
  const [inputValue, setInputValue] = useState('');

  const handleInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  return (
    <Center flex={1}>
      <VStack gap={6}>
        <Heading size="3xl">What prompt can I help you to improve?</Heading>
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
              <IconButton
                fontSize="2xl"
                size="sm"
                borderRadius="full"
                disabled={inputValue === ''}
              >
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
              value={inputValue}
              onChange={handleInputValue}
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
  );
}
